from modules.snmp.snmpEngine import SnmpEngine

class ManagedNode:
    def __init__(self, ipAddress, name="", snmpReadCommunity="public", snmpWriteComunity="private", credentials=None):
        self.snmpEngine = SnmpEngine(ipAddress, snmpReadCommunity, snmpWriteComunity, credentials)
        self.ipAddress = ipAddress
        self.name = self.snmpEngine.get('SNMPv2-MIB', 'sysName', 0, format='instSymbol:valPretty')['sysName']

    def getGlobalInfo(self, format="instSymbol:valPretty"):
        globalInfo = dict()
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysName', 0, format=format))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysLocation', 0, format=format))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysContact', 0, format=format))
        globalInfo.update(self.snmpEngine.get('SNMPv2-MIB', 'sysDescr', 0, format=format))
        return globalInfo

    def setLocation(self, descr, format="instSymbol:valPretty"):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysLocation', 0, format=format)

    def setContact(self, descr, format="instSymbol:valPretty"):
        return self.snmpEngine.set(descr, 'SNMPv2-MIB', 'sysContact', 0, format=format)
    