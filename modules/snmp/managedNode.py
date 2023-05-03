from modules.snmp.snmpEngine import SnmpEngine

class ManagedNode:
    def __init__(self, ipAddress, snmpReadCommunity="public", snmpWriteComunity="private", credentials=None):
        self.snmpEngine = SnmpEngine(ipAddress, snmpReadCommunity, snmpWriteComunity, credentials)
        self.ipAddress = ipAddress

    def getGlobalInfo(self, format="default"):
        globalInfo = dict()
        try:
            globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysName', 0, format=format))
            globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysDescr', 0, format=format))
            globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysLocation', 0, format=format))
            globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysContact', 0, format=format))
            return globalInfo
        except:
            pass

    def setLocation(self, descr, format="default"):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysLocation', 0, format=format)

    def setContact(self, descr, format="default"):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysContact', 0, format=format)
    