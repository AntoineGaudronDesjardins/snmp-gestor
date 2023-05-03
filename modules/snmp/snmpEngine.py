from modules.utils import createMibViewController, getOid, getTableColumns, formatter

from pysnmp.hlapi import SnmpEngine as Engine, UdpTransportTarget, ContextData
from pysnmp.hlapi import ObjectType, ObjectIdentity
from pysnmp.hlapi import CommunityData, UsmUserData
from pysnmp.hlapi import getCmd, nextCmd, bulkCmd, setCmd


class SnmpEngine:
    def __init__(self, agentIpAddress, readCommunity, writeCommunity, credentials):
        self.engine = Engine()
        self.transport = UdpTransportTarget((agentIpAddress, 161))
        self.context = ContextData()

        # Default communities
        self.communities = {
            "readCommunity" : CommunityData(readCommunity, mpModel=0),
            "writeCommunity" : CommunityData(writeCommunity, mpModel=0),
            readCommunity : CommunityData(readCommunity, mpModel=0),
            writeCommunity : CommunityData(writeCommunity, mpModel=0),
        }

        # Register declared users (SNMPv3)
        if credentials:
            self.users = {
                key : UsmUserData(key,
                    credentials[key]["authKey"],
                    credentials[key]["privKey"],
                    authProtocol=credentials[key]["authProtocol"],
                    privProtocol=credentials[key]["privProtocol"]
                ) for key in credentials
            }

        self.mibViewController = createMibViewController()
        self.engine.setUserContext(mibViewController=self.mibViewController)


    ######################################################################################
    ################################## Request methods ###################################
    ######################################################################################
    def get(self, mibName, objectName, *instanceIdentifier, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["readCommunity"]

        instance = ObjectType(ObjectIdentity(mibName, objectName, *instanceIdentifier))
        iterator = getCmd(self.engine, auth, self.transport, self.context, instance)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)
        
    
    def getByOID(self, oid, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["readCommunity"]

        instance = ObjectType(ObjectIdentity(oid))
        iterator = getCmd(self.engine, auth, self.transport, self.context, instance)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)
        
    
    def getNext(self, mibName, objectName, *instanceIdentifier, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["readCommunity"]

        initialObject = ObjectType(ObjectIdentity(mibName, objectName, *instanceIdentifier))
        iterator = nextCmd(self.engine, auth, self.transport, self.context, initialObject)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)
        
    
    def getNextByOID(self, oid, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["readCommunity"]

        initialObject = ObjectType(ObjectIdentity(oid))
        iterator = nextCmd(self.engine, auth, self.transport, self.context, initialObject)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)
    

    def getTable(self, mibName, tableName, *columns, startIndex=[], maxRepetitions=1000, auth=None, format="default"):        
        if not columns:
            columns = getTableColumns(self.mibViewController, mibName, tableName)
            columns = self._extractAccessibleObjects(mibName, *columns, auth=auth)
        if not columns:
            print(f'The table {tableName} is empty')
            return { tableName : [] }
        
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["readCommunity"]
        
        objectRequestedList = [ObjectType(ObjectIdentity(mibName, column, *startIndex)) for column in columns]
        if startIndex:
            firstRow = getCmd(self.engine, auth, self.transport, self.context, *objectRequestedList)
        iterator = bulkCmd(self.engine, auth, self.transport, self.context, 0, maxRepetitions, *objectRequestedList)

        columnOidCheck = getOid(self.mibViewController, mibName, columns[0])
        result = []
        for count in range(maxRepetitions):
            if startIndex and count == 0:
                row = next(firstRow)
            else:
                row = next(iterator)
            if not SnmpEngine.failedRequest(row):
                varBinds = row[3]
                if not str(varBinds[0][0]).startswith(str(columnOidCheck)):
                    break
                result.append(varBinds)
            else:
                break
        
        return { tableName : [formatter(self.mibViewController, row, format=format) for row in result] }


    def set(self, value, mibName, objectName, *instanceIdentifier, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["writeCommunity"]

        instance = ObjectType(ObjectIdentity(mibName, objectName, *instanceIdentifier), value)
        iterator = setCmd(self.engine, auth, self.transport, self.context, instance)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)


    def setTableRow(self, mibName, index, *args, auth=None, format="default"):
        if auth:
            if auth in self.communities:
                auth = self.communities[auth]
            elif auth in self.users:
                auth = self.users[auth]
        else:
            auth = self.communities["writeCommunity"]
        
        instances = []
        for arg in args:
            column, value = arg
            instances.append(ObjectType(ObjectIdentity(mibName, column, *index), value))
        
        iterator = setCmd(self.engine, auth, self.transport, self.context, *instances)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return formatter(self.mibViewController, varBinds, format=format)
    

    ######################################################################################
    ################################## Response handlers #################################
    ######################################################################################
    def failedRequest(response):
        errorIndication, errorStatus, errorIndex, varBinds = response

        if errorIndication:
            print(errorIndication)
            return True

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return True
        
        return False

    def _extractAccessibleObjects(self, mibName, *args, auth=None):
        accessibleObjects = []
        for obj in args:
            objOID = str(getOid(self.mibViewController, mibName, obj))
            res = self.getNext(mibName, obj, auth=auth)
            if not res:
                break
            resObjOID = str([*res.keys()][0].getOid())
            if resObjOID.startswith(objOID):
                accessibleObjects.append(obj)
        return accessibleObjects
    