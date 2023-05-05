
class Entry:
    def __init__(self, entry):
        self.index = [*entry['index'].values()]
        self.columns = entry['columns']
        self.entryStatus = None
        if "EntryStatus" in [*self.columns.keys()][-1]:
            self.entryStatus = [*self.columns.keys()][-1]
        # self.wildcarded = None
        self.multiplicity = 1
        self.instValIndex = []
        self.indexes = []
        self.args = []

    
    def resolve(self, snmpEngine):
        if (not self.indexes) or (not self.args):
            self._extend(snmpEngine)
        for i in range(self.multiplicity):
            for j in self.instValIndex:
                # if self.wildcarded:
                inst = self.args[i][j][1]
                if inst.oidFlag:
                    self.args[i][j] = (self.args[i][j][0], self.args[i][j][1].oids[i])
                else:
                    self.args[i][j] = (self.args[i][j][0], self.args[i][j][1].values[i])
                # else:

        # for i, (key, val) in enumerate(self.columns.items()):
        #     if isinstance(val, InstanceValue):
        #         self.wildcarded = val.wildcarded
        #         val = val.resolve(snmpEngine)
        #         if not self.wildcarded:
        #             self.columns[key] = val
        #             return self.index, [*self.columns.items()]
        #         else:
        #             self.columns = [[*self.columns.items()] for _ in range(len(val))]
        #             indexes = [self.index.copy() for _ in range(len(val))]
        #             for j in range(len(val)):
        #                 self.columns[j][i] = (self.columns[j][i][0], val[j])
        #                 indexes[j][-1] = f"{self.index[-1]}-{j}"
        #             self.index = indexes
        #             return self.index, self.columns
        
        # return self.index, [*self.columns.items()]

    
    def _extend(self, snmpEngine):
        for i, val in enumerate(self.columns.values()):
            if isinstance(val, Instance):
                self.instValIndex.append(i)
                val.resolve(snmpEngine)
                # self.wildcarded = val.wildcarded
                self.multiplicity = max(self.multiplicity, val.multiplicity)
                # val = val.resolve(snmpEngine)
                # if not val.wildcarded:
                    # self.args = [*self.columns.items()]
                    # self.columns[key] = val
                    # return self.index, [*self.columns.items()]
                # else:
                #     self.columns = [[*self.columns.items()] for _ in range(len(val))]
                #     indexes = [self.index.copy() for _ in range(len(val))]
                #     for j in range(len(val)):
                #         # self.columns[j][i] = (self.columns[j][i][0], val[j])
                #         indexes[j][-1] = f"{self.index[-1]}-{j}"
                #     self.index = indexes
                #     # return self.index, self.columns
            
            # if not self.wildcarded:
            #     self.args = [*self.columns.items()]
            #     # instValIndex.append(i)
            #     # self.columns[key] = val
            #     # return self.index, [*self.columns.items()]
            # else:
        self.args = [[*self.columns.items()] for _ in range(self.multiplicity)]
        self.indexes = [self.index.copy() for _ in range(self.multiplicity)]
        if self.multiplicity > 1:
            for j in range(self.multiplicity):
                # self.columns[j][i] = (self.columns[j][i][0], val[j])
                self.indexes[j][-1] = f"{self.index[-1]}{j}"
        # self.index = indexes
            # return self.index, self.columns
        self._extended = True
        # return self.index, [*self.columns.items()]



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
            resp = snmpEngine.walkByOID(self.refOid, format="OID")
            self.multiplicity = len(resp)
            self.oids = [oid for entry in resp for oid in entry.keys()]
            self.values = [self.callback(val) for entry in resp for val in entry.values()]
        else:
            resp = snmpEngine.getByOID(self.refOid, format="OID")
            self.multiplicity = 1
            self.oids = [self.refOid]
            self.values = [self.callback(resp[self.refOid])]
            # return self.callback(resp[self.oid])
    

    # def extend(self, entry, snmpEngine):
    #     index, columns = entry['index'], entry['columns']
    #     templateRow = [column_value for column_value in columns.items()]

    #     instancesValues = snmpEngine.walkByOID(self.oid, format="OID")[self.oid]

    #     entries = []
    #     for i, val in enumerate(instancesValues):
    #         newEntry = dict()
    #         newIndex = index.copy()
    #         newIndex[[newIndex.keys()][-1]] = f"{index[[index.keys()][-1]]}-{i}"
    #         newEntry["index"] = newIndex
    #         newEntry["args"] = [val if item is self else item for item in templateRow]
    #         entries.append(newEntry)
    #     return entries
    