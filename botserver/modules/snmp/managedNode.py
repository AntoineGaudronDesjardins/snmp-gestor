from modules.snmp.snmpEngine import SnmpEngine
from modules.snmp.mibNode import MibNode
from modules.snmp.table import Table

class ManagedNode:
    def __init__(self, ipAddress, snmpReadCommunity="public", snmpWriteComunity="private", credentials=None):
        self.snmpEngine = SnmpEngine(ipAddress, snmpReadCommunity, snmpWriteComunity, credentials)
        self.ipAddress = ipAddress
        # SNMPv2-MIB
        self.sysName = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysName', 0)).get()
        self.sysLocation = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).get()
        self.sysContact = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).get()
        self.sysDescr = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysDescr', 0)).get()
        # HOST-RESOURCES-MIB metrics
        self.hrSystemUptime = MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemUptime', 0))
        self.hrSystemProcesses = MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0))
        self.hrStorageTable = Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrStorageTable').pullData('hrStorageIndex', 'hrStorageUsed')
        self.hrProcessorTable = Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrProcessorTable').pullData('hrProcessorFrwID', 'hrProcessorLoad')
        # IF-MIB metrics
        self.ifTable = Table(self.snmpEngine, 'IF-MIB', 'ifTable').pullData('ifIndex', 'ifOperStatus', 'ifLastChange')
        
    
    @property
    def name(self):
        if not self.sysName.ok:
            self.sysName.get()
        return self.sysName.value if self.sysName.ok else "sin nombre"

    ######################################################################################
    ################################ Information methods #################################
    ######################################################################################
    def printGlobalInfo(self):
        globalInfo = []
        
        if not self.sysName.ok:
            self.sysName.get()
        if self.sysName.ok:
            globalInfo.append(self.sysName.print())
        
        if not self.sysLocation.ok:
            self.sysLocation.get()
        if self.sysLocation.ok:
            globalInfo.append(self.sysLocation.print())
        
        if not self.sysContact.ok:
            self.sysContact.get()
        if self.sysContact.ok:
            globalInfo.append(self.sysContact.print())
        
        if not self.sysDescr.ok:
            self.sysDescr.get()
        if self.sysDescr.ok:
            globalInfo.append(self.sysDescr.print())
        
        return globalInfo
    

    def printHealthMetrics(self):
        healthMetrics = []
        
        # HOST-RESOURCES-MIB metrics
        if self.hrSystemUptime.get().ok:
            healthMetrics.append(self.hrSystemUptime.print())
        
        if self.hrSystemProcesses.get().ok:
            healthMetrics.append(self.hrSystemProcesses.print())

        if self.hrStorageTable.refresh().ok:
            healthMetrics.append(self.hrStorageTable.print(index=False))
        
        if self.hrProcessorTable.refresh().ok:
            healthMetrics.append(self.hrProcessorTable.print(index=False))

        # IF-MIB metrics
        if self.ifTable.refresh().ok:
            healthMetrics.append(self.ifTable.print(index=False))
        
        return healthMetrics
    
    
    ######################################################################################
    ############################### Basic setters methods ################################
    ######################################################################################
    def setLocation(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).set(descr).ok


    def setContact(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).set(descr).ok
    

    ######################################################################################
    ################################# Auxiliary methods ##################################
    ######################################################################################
    def registerBot(self, bot):
        self.bot = bot
    
    
    def triggerAlert(self, title, desc):
        if self.bot:
            self.bot.sendAlert(self.ipAddress, title, desc)