from modules.snmp.snmpEngine import SnmpEngine
from modules.snmp.mibNode import MibNode

class ManagedNode:
    def __init__(self, ipAddress, snmpReadCommunity="public", snmpWriteComunity="private", credentials=None):
        self.snmpEngine = SnmpEngine(ipAddress, snmpReadCommunity, snmpWriteComunity, credentials)
        self.ipAddress = ipAddress
        self.name = MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysName', 0)).get()

    def getGlobalInfo(self):
        globalInfo = []
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysName', 0)).get())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).get())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).get())
        globalInfo.append(MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysDescr', 0)).get())
        return globalInfo

    def setLocation(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysLocation', 0)).set(descr)

    def setContact(self, descr):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'sysContact', 0)).set(descr)
    