from modules.utils import createMibViewController
from modules.snmp.table import Table
from modules.snmp.mibNode import MibNode

from pysnmp.hlapi import SnmpEngine as Engine, UdpTransportTarget, ContextData
from pysnmp.hlapi import ObjectType, ObjectIdentity
from pysnmp.hlapi import CommunityData, UsmUserData
from pysnmp.hlapi import getCmd, nextCmd, bulkCmd, setCmd


class SnmpEngine:
    def __init__(self, agentIpAddress, readCommunity, writeCommunity, credentials):
        self.engine = Engine()
        self.transport = UdpTransportTarget((agentIpAddress, 161), timeout=10, retries=5)
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
    def get(self, inst, auth):
        sess = self._getSession(auth, rw=False)
        iterator = getCmd(self.engine, sess, self.transport, self.context, inst)
        response = next(iterator)
        varBinds = self._extractResponse(response)
        return varBinds[0] if varBinds and len(varBinds)==1 else None
        
    
    def getNext(self, obj, auth):
        sess = self._getSession(auth, rw=False)
        iterator = nextCmd(self.engine, sess, self.transport, self.context, obj)
        response = next(iterator)
        varBinds = self._extractResponse(response)
        return varBinds[0] if varBinds and len(varBinds)==1 else None


    def set(self, inst, auth):
        sess = self._getSession(auth, rw=True)
        iterator = setCmd(self.engine, sess, self.transport, self.context, inst)
        response = next(iterator)
        varBinds = self._extractResponse(response)
        return varBinds[0] if varBinds and len(varBinds)==1 else None
    

    def walk(self, scalar, auth):
        sess = self._getSession(auth, rw=False)
        res, _ = self._walkRecursive(scalar, sess)
        return res
    

    ######################################################################################
    ################################# Gestion de tablas ##################################
    ######################################################################################
    def getTable(self, columns, maxRepetitions, auth, includeFirst, check):
        sess = self._getSession(auth, rw=False)

        if includeFirst:
            firstRow = getCmd(self.engine, sess, self.transport, self.context, *columns)
        iterator = bulkCmd(self.engine, sess, self.transport, self.context, 0, maxRepetitions, *columns)

        indexes = []
        result = []
        for count in range(maxRepetitions):
            if includeFirst and count == 0:
                row = next(firstRow)
            else:
                row = next(iterator)

            varBinds = self._extractResponse(row)
            ok, index = check(varBinds)
            if ok:
                result.append(varBinds)
                indexes.append(index)
            else:
                break
        return result, indexes


    def setTableRow(self, instances, auth):
        sess = self._getSession(auth, rw=True)
        iterator = setCmd(self.engine, sess, self.transport, self.context, *instances)
        response = next(iterator)
        return self._extractResponse(response)
    

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
    

    def _extractResponse(self, res):
        errorIndication, errorStatus, errorIndex, varBinds = res

        if errorIndication:
            print(errorIndication)
            return
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0].prettyPrint() or '?'))
            return
        
        return varBinds
    

    def _walkRecursive(self, scalar, sess):
        mib, symb, index = scalar.getMibSymbol()
        _, prevSymbol, _ = scalar.getParent().getMibSymbol()

        lastScalar = scalar.getNext()
        if not lastScalar:
            print("No more instance in this view")
            return None, None
        _, nextSymb, _ = lastScalar.getMibSymbol()

        if symb.endswith("Table") or prevSymbol.endswith("Table"):
            if symb.endswith("Table"):
                tableName = symb
            else:
                tableName = prevSymbol
            resultIndex = MibNode(self, (mib, tableName))
            result = Table(self, mib, tableName).pullData()
            lastScalar = result.getNext()
        
        elif index or (symb == nextSymb):
            if prevSymbol.endswith("Entry"):
                _, tableName, _ = scalar.getParent().getParent().getMibSymbol()
                resultIndex = MibNode(self, (mib, symb))
                result = Table(self, mib, tableName).pullData(symb)
                lastScalar = result.getNext()
            else:
                resultIndex = MibNode(self, (mib, symb))
                result = lastScalar.get()
                lastScalar = result.getNext()
        
        else:
            if not scalar.isParent(lastScalar):
                result = None
            
            else:
                resultIndex = scalar
                result = dict()
                length = len(scalar)
                nextScalar = lastScalar.getParent(length+1)
                while nextScalar:
                    subTree, lastScalar = self._walkRecursive(nextScalar, sess)
                    if subTree:
                        result.update(subTree)

                    if not lastScalar:
                        print("No more instance in this view")
                        nextScalar = None
                    elif scalar.isParent(lastScalar):
                            nextScalar = lastScalar.getParent(length+1)
                    else:
                        nextScalar = None
                    
        return None if not result else { resultIndex : result }, lastScalar
