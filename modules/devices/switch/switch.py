from modules.devices.switch.switchTrapConfig import switchTrapConfig
from modules.devices.switch.credentials import credentials
from modules.snmp import ManagedNode
from modules.utils import InstanceValue, Entry


class Switch(ManagedNode):
    def __init__(self, ipAddress):
        ManagedNode.__init__(self, ipAddress, credentials=credentials)


    def getHealthMetrics(self, format="default"):
        healthMetrics = dict()
        # HOST-RESOURCES-MIB metrics
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemUptime', 0, format=format))
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0, format=format))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrStorageTable', 'hrStorageIndex', 'hrStorageUsed', format=format))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrProcessorTable', 'hrProcessorFrwID', 'hrProcessorLoad', format=format))
        # IF-MIB metrics
        healthMetrics.update(self.snmpEngine.getTable('IF-MIB', 'ifTable', 'ifIndex', 'ifOperStatus', 'ifLastChange', format=format))
        return healthMetrics
    

    def initTraps(self):

        def initDismanTable(tableName):
            for entry in switchTrapConfig[tableName]:
                newRow = Entry(entry)
                
                print("Checking for existing entry...")
                existingRow = self.snmpEngine.getTable('DISMAN-EVENT-MIB', tableName, startIndex=newRow.index, maxRepetitions=1, format="valueOID")[tableName]
                
                if existingRow and newRow.entryStatus:
                    print("Deleting old entry...")
                    self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', newRow.index, (newRow.entryStatus, 'destroy'), auth="antoine")

                index, entry = newRow.resolve(self.snmpEngine)
                if newRow.wildcarded:
                    for ind, row in zip(index, entry):
                        print(ind, row)
                        newRow = self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', ind, *row, auth="antoine")
                        if not newRow: 
                            print(f"Failed to create new entry in table {tableName}")
                else:
                    print("Creating new entry...")
                    newRow = self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', index, *entry, auth="antoine")
                    if not newRow: 
                        print(f"Failed to create new entry in table {tableName}")


            print(f'Table {tableName} has been updated')
        
        initDismanTable('mteObjectsTable')
        initDismanTable('mteTriggerTable')
        initDismanTable('mteTriggerExistenceTable')
        initDismanTable('mteTriggerBooleanTable')
        initDismanTable('mteTriggerThresholdTable')
        initDismanTable('mteTriggerDeltaTable')
        initDismanTable('mteEventTable')
        initDismanTable('mteEventNotificationTable')
        initDismanTable('mteEventSetTable')

        for entry in switchTrapConfig['mteTriggerTable']:
            self.snmpEngine.set('active', 'DISMAN-EVENT-MIB', 'mteTriggerEntryStatus', *entry["index"].values(), auth="antoine")
        
        for entry in switchTrapConfig['mteEventTable']:
            self.snmpEngine.set('active', 'DISMAN-EVENT-MIB', 'mteEventEntryStatus', *entry["index"].values(), auth="antoine")
        