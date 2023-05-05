from pysnmp.proto.rfc1902 import Bits


class NamedBits:
    bits = { 0: Bits('\x80'), 1: Bits('\x40'), 2: Bits('\x20'), 3: Bits('\x10'), 4: Bits('\x08'), 5: Bits('\x04'), 6: Bits('\x02'), 7: Bits('\x01') }

    def __init__(self, nameDict):
        self.namedBits = { name : self.bits[i] for name, i in nameDict.items()}

    def __getitem__(self, name):
        return self.bits[name]

    def __getitem__(self, key):
        if key.startswith("UnknownBit-"):
            return [*self.namedBits.keys()][int(key[-1])]
        return self.namedBits[key]
    


class Instance:
    def __init__(self, refOid, callback=lambda x: x, wildcarded=False, oidFlag=False):
        self.refOid = refOid
        self.wildcarded = wildcarded
        self.oidFlag = oidFlag
        self.callback = callback
        self.multiplicity = 0
        self.values = []
        self.oids = []
    
    def resolve(self, snmpEngine):
        if self.wildcarded:
            resp = snmpEngine.walkByOID(self.refOid, format="instOID:valOID")
            self.multiplicity = len(resp)
            self.oids = [oid for entry in resp for oid in entry.keys()]
            self.values = [self.callback(val) for entry in resp for val in entry.values()]
        else:
            resp = snmpEngine.getByOID(self.refOid, format="instOID:valOID")
            self.multiplicity = 1
            self.oids = [self.refOid]
            self.values = [self.callback(resp[self.refOid])]



class Entry:
    def __init__(self, entry):
        self.index = [*entry['index'].values()]
        self.columns = entry['columns']
        self.entryStatus = None
        if "EntryStatus" in [*self.columns.keys()][-1]:
            self.entryStatus = [*self.columns.keys()][-1]
        self.multiplicity = 1
        self.instValIndex = []
        self.indexes = []
        self.args = []

    def resolve(self, snmpEngine):
        if (not self.indexes) or (not self.args):
            self._extend(snmpEngine)
        for i in range(self.multiplicity):
            for j in self.instValIndex:
                inst = self.args[i][j][1]
                if inst.oidFlag:
                    self.args[i][j] = (self.args[i][j][0], self.args[i][j][1].oids[i])
                else:
                    self.args[i][j] = (self.args[i][j][0], self.args[i][j][1].values[i])

    def _extend(self, snmpEngine):
        for i, val in enumerate(self.columns.values()):
            if isinstance(val, Instance):
                self.instValIndex.append(i)
                val.resolve(snmpEngine)
                self.multiplicity = max(self.multiplicity, val.multiplicity)
        
        self.args = [[*self.columns.items()] for _ in range(self.multiplicity)]
        self.indexes = [self.index.copy() for _ in range(self.multiplicity)]
        if self.multiplicity > 1:
            for j in range(self.multiplicity):
                self.indexes[j][-1] = f"{self.index[-1]}{j}"
