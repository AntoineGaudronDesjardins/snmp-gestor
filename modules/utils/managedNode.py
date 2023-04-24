from modules.utils import SnmpEngine

class ManagedNode:
    def __init__(self, ipAddress, SnmpCommunity="public"):
        self.snmpEngine = SnmpEngine(ipAddress, SnmpCommunity)

    def run(self):
        pass

    def getGlobalInfo(self):
        globalInfo = dict()
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysName', 0))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysDescr', 0))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysLocation', 0))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysContact', 0))
        return globalInfo

    def setLocation(self, descr):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysLocation', 0)

    def setContact(self, descr):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysContact', 0)
    