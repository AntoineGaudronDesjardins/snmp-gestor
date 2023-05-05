
class Entry:
    def __init__(self, entry):
        self.index = [*entry['index'].values()]
        self.columns = entry['columns']
        self.wildcarded = None
        self.entryStatus = None
        if "EntryStatus" in [*self.columns.keys()][-1]:
            self.entryStatus = [*self.columns.keys()][-1]

    
    def resolve(self, snmpEngine):
        for i, (key, val) in enumerate(self.columns.items()):
            if isinstance(val, InstanceValue):
                self.wildcarded = val.wildcarded
                val = val.resolve(snmpEngine)
                if not self.wildcarded:
                    self.columns[key] = val
                    return self.index, [*self.columns.items()]
                else:
                    self.columns = [[*self.columns.items()] for _ in range(len(val))]
                    indexes = [self.index.copy() for _ in range(len(val))]
                    for j in range(len(val)):
                        self.columns[j][i] = (self.columns[j][i][0], val[j])
                        indexes[j][-1] = f"{self.index[-1]}-{j}"
                    self.index = indexes
                    return self.index, self.columns
        
        return self.index, [*self.columns.items()]



class InstanceValue:
    def __init__(self, oid, refOid, callback=lambda x: x, wildcarded=False):
        self.oid = oid
        self.refOid = refOid
        self.wildcarded = wildcarded
        self.callback = callback
        self.multiplicity = 1
    
    def resolve(self, snmpEngine):
        if self.wildcarded:
            resp = snmpEngine.walkByOID(self.oid, format="OID")
            return [self.callback(val) for entry in resp for val in entry.values()]
        else:
            resp = snmpEngine.getByOID(self.oid)
            return self.callback(resp[self.oid])
    

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
    