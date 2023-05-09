from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from modules.utils import formatter


class MibNode:
    def __init__(self, snmpEngine, identifier):
        self.engine = snmpEngine
        self.mibs = snmpEngine.mibViewController
        if isinstance(identifier, ObjectType):
            self.varBind = identifier
        elif isinstance(identifier, tuple) or isinstance(identifier, list):
            self.varBind = ObjectType(ObjectIdentity(*identifier))
        else:
            self.varBind = ObjectType(ObjectIdentity(identifier))
        self.varBind.resolveWithMib(self.mibs)
    

    ######################################################################################
    ################################## Request methods ###################################
    ######################################################################################
    def get(self, auth=None):
        self.varBind = self.engine.get(self.varBind, auth)
        return self
    

    def getNext(self, auth=None):
        varBind = self.engine.getNext(self.varBind, auth)
        if varBind:
            return MibNode(self.engine, varBind)


    def set(self, value, auth=None):
        self.varBind = ObjectType(self.varBind[0], value)
        self.varBind = self.engine.set(self.varBind, auth)
        return self
    

    ######################################################################################
    ############################# SNMP walk specific methods #############################
    ######################################################################################
    def walk(self, auth=None):
        return self.engine.walk(self, auth)
    

    def getParent(self, n=None):
        n = n if n else len(self)-1
        parentOid = ".".join(str(self.varBind[0].getOid()).split(".")[:n])
        return MibNode(self.engine, parentOid)
    

    def isParent(self, scalar):
        return str(scalar.varBind[0].getOid()).startswith(str(self.varBind[0].getOid()))


    ######################################################################################
    ################################### Render methods ###################################
    ######################################################################################
    def format(self, pattern):
        return formatter(self.mibs, [self.varBind], format=pattern)


    def __repr__(self):
        _, symbol, _ = self.getMibSymbol()
        return f"``` {symbol} = {self.varBind[1].prettyPrint()} ```\n\n"
    

    ######################################################################################
    ################################## Internal methods ##################################
    ######################################################################################
    def __len__(self):
        return len(str(self.varBind[0].getOid()).split("."))
    
    def __getitem__(self, key):
        if key in [0, 1]:
            return self.varBind[key]
        elif key=="oid":
            return str(self.varBind[0].getOid())
    
    def getMibSymbol(self):
        return self.varBind[0].getMibSymbol()