from modules.snmp.snmpEngine import SnmpEngine
from modules.snmp.mibNode import MibNode
from modules.snmp.table import Table

class ManagedNode:
    def __init__(self, ipAddress, snmpReadCommunity="public", snmpWriteComunity="private", credentials=None):
        self.snmpEngine = SnmpEngine(ipAddress, snmpReadCommunity, snmpWriteComunity, credentials)
        self.ipAddress = ipAddress
        self.name = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysName', 0)).get().value
    

    ######################################################################################
    ################################ Information methods #################################
    ######################################################################################
    def printGlobalInfo(self):
        globalInfo = []
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysName', 0)).get().print())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).get().print())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).get().print())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysDescr', 0)).get().print())
        return globalInfo
    

    def printHealthMetrics(self):
        healthMetrics = []
        # HOST-RESOURCES-MIB metrics
        healthMetrics.append(MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemUptime', 0)).get().print())
        healthMetrics.append(MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0)).get().print())
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrStorageTable').pullData('hrStorageIndex', 'hrStorageUsed').print(index=False))
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrProcessorTable').pullData('hrProcessorFrwID', 'hrProcessorLoad').print(index=False))
        # IF-MIB metrics
        healthMetrics.append(Table(self.snmpEngine, 'IF-MIB', 'ifTable').pullData('ifIndex', 'ifOperStatus', 'ifLastChange').print(index=False))
        return healthMetrics
    
    
    ######################################################################################
    ############################### Basic setters methods ################################
    ######################################################################################
    def setLocation(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).set(descr)

    def setContact(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).set(descr)
    

    ######################################################################################
    ################################# Auxiliary methods ##################################
    ######################################################################################
    def registerBot(self, bot):
        self.bot = bot
    
    
    def triggerAlert(self, title, desc):
        if self.bot:
            self.bot.sendAlert(self.ipAddress, title, desc)