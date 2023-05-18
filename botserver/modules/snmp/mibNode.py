from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from modules.utils import formatter


class MibNode:
    def __init__(self, snmpEngine, identifier, mibs=None):
        self.engine = snmpEngine
        self.mibs = mibs if mibs else snmpEngine.mibViewController
        if isinstance(identifier, ObjectType):
            self.varBind = identifier
        elif isinstance(identifier, tuple) or isinstance(identifier, list):
            self.varBind = ObjectType(ObjectIdentity(*identifier))
        else:
            self.varBind = ObjectType(ObjectIdentity(identifier))
        self.varBind.resolveWithMib(self.mibs)
        self.querySuccess = False
    

    @property
    def oid(self):
        return str(self.varBind[0].getOid())
    
    @property
    def value(self):
        value = self.varBind[1].prettyPrint()
        if value.isdigit():
            value = int(value)
        return value
    
    @property
    def ok(self):
        return self.querySuccess

    ######################################################################################
    ################################## Request methods ###################################
    ######################################################################################
    def get(self, auth=None):
        self.querySuccess = False
        res = self.engine.get(self.varBind, auth)
        if res:
            self.varBind = res
            self.querySuccess = True
        return self
    

    def getNext(self, auth=None):
        self.querySuccess = False
        varBind = self.engine.getNext(self.varBind, auth)
        if varBind:
            self.querySuccess = True
            return MibNode(self.engine, varBind)


    def set(self, value, auth=None):
        self.querySuccess = False
        newInst = ObjectType(self.varBind[0], value)
        res = self.engine.set(newInst, auth)
        if res:
            self.varBind = res
            self.querySuccess = True
        return self
    

    ######################################################################################
    ############################# SNMP walk specific methods #############################
    ######################################################################################
    def walk(self, auth=None):
        return self.engine.walk(self, auth)
    

    def getParent(self, n=None):
        n = n if n else len(self)-1
        parentOid = ".".join(self.oid.split(".")[:n])
        return MibNode(self.engine, parentOid)
    

    def isParent(self, scalar):
        return scalar.oid.startswith(self.oid)


    ######################################################################################
    ################################### Render methods ###################################
    ######################################################################################
    def format(self, pattern):
        return formatter(self.mibs, [self.varBind], format=pattern)


    def print(self, symbol=True, index=False):
        if symbol:
            _, symb, ind = self.getMibSymbol()
            if index:
                symb = f"{symb}.{ind[0]}"
            return f" {symb} = {self.value} "
        else:
            return str(self.value)


    def __repr__(self):
        return self.print()
    
    ######################################################################################
    ################################## Internal methods ##################################
    ######################################################################################
    def __len__(self):
        return len(self.oid.split("."))
    
    def __getitem__(self, key):
        if key in [0, 1]:
            return self.varBind[key]
    
    def getMibSymbol(self):
        return self.varBind[0].getMibSymbol()