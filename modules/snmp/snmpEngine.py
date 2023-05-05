from modules.utils import createMibViewController, getOid, getTableColumns, formatter, getMibSymbol

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
        oid = getOid(self.mibViewController, mibName, objectName, *instanceIdentifier, stringify=True)
        return self.getByOID(oid, auth, format)
        
    
    def getByOID(self, oid, auth=None, format="default"):
        sess = self._getSession(auth, rw=False)

        instance = ObjectType(ObjectIdentity(oid))
        iterator = getCmd(self.engine, sess, self.transport, self.context, instance)

        response = next(iterator)
        return self._extractResponse(response, format)
        
    
    def getNext(self, mibName, objectName, *instanceIdentifier, auth=None, format="default"):
        oid = getOid(self.mibViewController, mibName, objectName, *instanceIdentifier, stringify=True)
        return self.getNextByOID(oid, auth, format)
        
    
    def getNextByOID(self, oid, auth=None, format="default"):
        sess = self._getSession(auth, rw=False)

        initialObject = ObjectType(ObjectIdentity(oid))
        iterator = nextCmd(self.engine, sess, self.transport, self.context, initialObject)

        response = next(iterator)
        return self._extractResponse(response, format)
    

    def getTable(self, mibName, tableName, *columns, startIndex=[], maxRepetitions=1000, auth=None, format="default"):
        sess = self._getSession(auth, rw=False)

        if not columns:
            columns = getTableColumns(self.mibViewController, mibName, tableName)
            columns = self._extractAccessibleObjects(mibName, *columns, auth=auth)
            if not columns:
                print(f'The table {tableName} is empty')
                return { tableName : [] }
        
        objectRequestedList = [ObjectType(ObjectIdentity(mibName, column, *startIndex)) for column in columns]
        if startIndex:
            firstRow = getCmd(self.engine, sess, self.transport, self.context, *objectRequestedList)
        iterator = bulkCmd(self.engine, sess, self.transport, self.context, 0, maxRepetitions, *objectRequestedList)

        result = []
        for count in range(maxRepetitions):
            if startIndex and count == 0:
                row = next(firstRow)
            else:
                row = next(iterator)
            varBinds = self._extractResponse(row, format=None)

            if not varBinds: break

            varBindsSymb = formatter(self.mibViewController, varBinds, format="symbol")
            if not self._matchBaseOid(varBindsSymb.keys(), columns, symbol=True):
                break
            else:
                result.append(varBinds)
        
        return { tableName : [formatter(self.mibViewController, row, format=format) for row in result] }
    

    def walk(self, mibName, objectName=None, *instanceIdentifier, auth=None, format="default"):
        oid = getOid(self.mibViewController, mibName, objectName, *instanceIdentifier, stringify=True)
        return self.walkByOID(oid, auth, format)
    

    def walkByOID(self, oid, auth=None, format="default"):
        sess = self._getSession(auth, rw=False)
        res, _ = self._walkRecursive(oid, sess, format=format)
        return res


    def set(self, value, mibName, objectName, *instanceIdentifier, auth=None, format="default"):
        oid = getOid(self.mibViewController, mibName, objectName, *instanceIdentifier, stringify=True)
        return self.setByOID(value, oid, auth, format)


    def setByOID(self, value, oid, auth=None, format="default"):
        sess = self._getSession(auth, rw=True)

        instance = ObjectType(ObjectIdentity(oid), value)
        iterator = setCmd(self.engine, sess, self.transport, self.context, instance)

        response = next(iterator)
        return self._extractResponse(response, format)


    def setTableRow(self, mibName, index, *args, auth=None, format="default"):
        sess = self._getSession(auth, rw=True)
        
        instances = [ObjectType(ObjectIdentity(mibName, column, *index), value) for column, value in args]        
        iterator = setCmd(self.engine, sess, self.transport, self.context, *instances)

        response = next(iterator)
        return self._extractResponse(response, format)
    

    ######################################################################################
    ################################## Internal methods ##################################
    ######################################################################################
    def _getSession(self, auth, rw):
        if auth:
            if auth in self.communities:
                session = self.communities[auth]
            elif auth in self.users:
                session = self.users[auth]
        elif rw:
            session = self.communities["writeCommunity"]
        else:
            session = self.communities["readCommunity"]
        return session
    

    def _extractResponse(self, res, format):
        errorIndication, errorStatus, errorIndex, varBinds = res

        if errorIndication:
            print(errorIndication)
            return
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return
        
        return formatter(self.mibViewController, varBinds, format=format)
    
    
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
    

    def _matchBaseOid(self, varBinds, oids, symbol=False):
        if symbol:
            if set(varBinds) <= set(oids):
                return True
            return False
        
        else:
            for key in varBinds:
                if not any(key.startswith(oid) for oid in oids):
                    return False
            return True
    

    def _walkRecursive(self, oid, sess, format="default"):
        initialObject = ObjectType(ObjectIdentity(oid))
        iterator = nextCmd(self.engine, sess, self.transport, self.context, initialObject)
        response = next(iterator)
        varBinds = self._extractResponse(response, format=None)

        if varBinds:
            _, initSymbol, _ = getMibSymbol(self.mibViewController, oid)
            _, resSymbol, _ = getMibSymbol(self.mibViewController, str(varBinds[0][0]))

            if not str(varBinds[0][0]).startswith(oid):
                return None, str(varBinds[0][0])
            
            elif initSymbol == resSymbol:
                result = [formatter(self.mibViewController, varBinds, format=format)]
                response = next(iterator)
                varBinds = self._extractResponse(response, format=None)
                while varBinds and str(varBinds[0][0]).startswith(oid):
                    result.append(formatter(self.mibViewController, varBinds, format=format))
                    response = next(iterator)
                    varBinds = self._extractResponse(response, format=None)
                if len(result) == 1:
                    result = result[0]
                return result, str(varBinds[0][0])

            else:
                index = [*formatter(self.mibViewController, (initialObject, initialObject), format=format).keys()][0]
                if initSymbol.endswith("Entry"):
                    result = { index : list() }
                else:
                    result = { index : dict() }
                
                length = len(oid.split("."))
                nextOid = ".".join(str(varBinds[0][0]).split(".")[:length+1])
                lastOid = nextOid
                while nextOid:
                    subTree, lastOid = self._walkRecursive(nextOid, sess, format=format)

                    if subTree:
                        if isinstance(subTree, list):
                            if lastOid.startswith(oid):
                                result[index].append(subTree)
                            else:
                                table = [dict() for _ in range(len(subTree))]
                                for i in range(len(subTree)):
                                    for j in range(len(result[index])):
                                        table[i].update(result[index][j][i])
                                result[index] = table
                                    
                        else:
                            result[index].update(subTree)

                    if lastOid.startswith(oid):
                        nextOid = ".".join(lastOid.split(".")[:length+1])
                    else:
                        nextOid = None
                    
                return result, lastOid
            
        print("No more instance in this view")
        return result, None