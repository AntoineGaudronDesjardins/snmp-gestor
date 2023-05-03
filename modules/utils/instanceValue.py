class InstanceValue:
    def __init__(self, oid, callback=lambda x: x, wildcarded=False):
        self.oid = oid
        self.wildcarded = wildcarded
        self.callback = callback
    
    def resolve(self, snmpEngine):
        if self.wildcarded:
            res = snmpEngine.getNextByOID(self.oid)
        else:
            res = snmpEngine.getByOID(self.oid)
        
        res = [*res.values()][0].prettyPrint()

        if res.isdigit():
            res = int(res)

        return self.callback(res)
    