from pysnmp.proto.rfc1902 import Bits
from modules.snmp.mibNode import MibNode

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
    def __init__(self, oid, callback=lambda x: x, wildcarded=False, oidFlag=False):
        self.oid = oid
        self.wildcarded = wildcarded
        self.oidFlag = oidFlag
        self.callback = callback
        self.multiplicity = 0
        self.values = []
        self.oids = []
    
    def resolve(self, snmpEngine):
        scalar = MibNode(snmpEngine, self.oid)
        if self.wildcarded:
            tableColumn = [*scalar.walk().values()][0]
            self.multiplicity = len(tableColumn)
            self.oids = [str(row[0][0].getOid()) for row in tableColumn]
            self.values = [self.callback(row[0][1].prettyPrint()) for row in tableColumn]
        else:
            scalar = MibNode(snmpEngine, self.oid).get()
            self.multiplicity = 1
            self.oids = [self.oid]
            self.values = [self.callback(scalar.value if scalar.ok else 0)]



class Entry:
    def __init__(self, entry):
        self.index = [*entry['index'].values()]
        self.columns = entry['columns']
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
                    self.args[i][j] = (self.args[i][j][0], inst.oids[i])
                else:
                    self.args[i][j] = (self.args[i][j][0], inst.values[i])

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
