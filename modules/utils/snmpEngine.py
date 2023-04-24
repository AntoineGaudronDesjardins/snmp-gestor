from pysnmp.hlapi import SnmpEngine as Engine, UdpTransportTarget, ContextData
from pysnmp.hlapi import ObjectType, ObjectIdentity
from pysnmp.hlapi import CommunityData
from pysnmp.hlapi import getCmd, bulkCmd, setCmd
from pysnmp.smi import builder, view
import os


class SnmpEngine:
    def __init__(self, agentIpAddress, readCommunity='public', writeCommunity='private'):
        self.engine = Engine()
        self.communities = {
            readCommunity : CommunityData(readCommunity, mpModel=0),
            writeCommunity : CommunityData(writeCommunity, mpModel=0),
        }
        self.transport = UdpTransportTarget((agentIpAddress, 161))
        self.context = ContextData()

        mibBuilder = self.engine.getMibBuilder()
        mibBuilder.addMibSources(builder.DirMibSource(os.path.join(os.getcwd(), 'mibs')))
        self.mibViewController = self.engine.getUserContext('mibViewController')
        if not self.mibViewController:
            self.mibViewController = view.MibViewController(mibBuilder)
            self.engine.setUserContext(mibViewController=self.mibViewController)


    ######################################################################################
    ################################## Request methods ###################################
    ######################################################################################
    def get(self, MIBName, objectName, *instanceIdentifiers, community='public'):
        if not community in self.communities.keys():
            self.addCommunity(community)
        community = self.communities[community]

        instance = ObjectType(ObjectIdentity(MIBName, objectName, *instanceIdentifiers))
        iterator = getCmd(self.engine, community, self.transport, self.context, instance)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return SnmpEngine.format(varBinds)[0]
    

    def getTable(self, MIBName, tableName, *columns, community='public', maxRepetitions=1000):
        columnOidCheck = self.getOid(MIBName, columns[0])

        if not community in self.communities.keys():
            self.addCommunity(community)
        community = self.communities[community]

        objectRequestedList = [ObjectType(ObjectIdentity(MIBName, column)) for column in columns]
        iterator = bulkCmd(self.engine, community, self.transport, self.context, 0, maxRepetitions, *objectRequestedList)

        result = []
        for _i in range(maxRepetitions):
            row = next(iterator)
            if not SnmpEngine.failedRequest(row):
                varBinds = row[3]
                if not str(varBinds[0][0]).startswith(str(columnOidCheck)):
                    break
                result.append(varBinds)
            else:
                break
        
        return { tableName : [SnmpEngine.format(x) for x in result] }


    def set(self, value, MIBName, objectName, *instanceIdentifiers, community='private'):
        if not community in self.communities.keys():
            self.addCommunity(community)
        community = self.communities[community]

        instance = ObjectType(ObjectIdentity(MIBName, objectName, *instanceIdentifiers), value)
        iterator = setCmd(self.engine, community, self.transport, self.context, instance)

        response = next(iterator)
        if not SnmpEngine.failedRequest(response):
            varBinds = response[3]
            return SnmpEngine.format(varBinds)[0]

    
    def trap(self):
        pass
    

    ######################################################################################
    ################################# Community manager###################################
    ######################################################################################
    def addCommunity(self, community):
        self.communities[community] = CommunityData(community, mpModel=0)
    

    ######################################################################################
    ################################### Mib resolvers ####################################
    ######################################################################################
    def getOid(self, *args):
        return ObjectIdentity(*args).resolveWithMib(self.mibViewController).getOid()


    def getMibSymbol(self, oid):
        return ObjectIdentity(oid).resolveWithMib(self.mibViewController).getMibSymbol()
    

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


    def format(*varBinds):
        formatted = []
        for varBind in varBinds:
            for name, value in varBind:
                formatted.append({name.prettyPrint(): value.prettyPrint()})
        return formatted