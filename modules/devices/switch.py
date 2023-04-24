from modules.utils import ManagedNode

class Switch(ManagedNode):

    def getHealthMetrics(self):
        healthMetrics = dict()
        # HOST-RESOURCES-MIB metrics
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemUptime', 0))
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrStorageTable', 'hrStorageIndex', 'hrStorageUsed'))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrProcessorTable', 'hrProcessorFrwID', 'hrProcessorLoad'))
        # IF-MIB metrics
        healthMetrics.update(self.snmpEngine.getTable('IF-MIB', 'ifTable', 'ifIndex', 'ifOperStatus', 'ifLastChange'))
        return healthMetrics