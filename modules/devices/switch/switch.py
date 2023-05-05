from modules.devices.switch.switchTrapConfig import switchTrapConfig
from modules.devices.switch.credentials import credentials
from modules.snmp import ManagedNode
from modules.utils import Instance, Entry, getTableColumns


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
    

    def initTrapsConfig(self):
        self.clearTrapsConfig()

        def initDismanTable(tableName):
            for entry in switchTrapConfig[tableName]:
                newRow = Entry(entry)
                newRow.resolve(self.snmpEngine)
                for index, args in zip(newRow.indexes, newRow.args):
                    print("Creating new entry...")
                    newRow = self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', index, *args, auth="antoine")
                    if not newRow: 
                        print(f"Failed to create new entry in table {tableName}")

            print(f'Table {tableName} has been updated')
        
        initDismanTable('mteObjectsTable')
        initDismanTable('mteEventTable')
        initDismanTable('mteEventNotificationTable')
        initDismanTable('mteEventSetTable')
        initDismanTable('mteTriggerTable')
        initDismanTable('mteTriggerExistenceTable')
        initDismanTable('mteTriggerBooleanTable')
        initDismanTable('mteTriggerThresholdTable')
        initDismanTable('mteTriggerDeltaTable')

        self.activateAllEntries()
    

    def clearTrapsConfig(self):

        def clearDismanTable(tableName):
            entryStatus = getTableColumns(self.snmpEngine.mibViewController, 'DISMAN-EVENT-MIB', tableName)[-1]
            controlColumn = self.snmpEngine.getTable('DISMAN-EVENT-MIB', tableName, entryStatus)[tableName]

            for entry in controlColumn:
                print("Deleting entry...")
                self.snmpEngine.setByOID('destroy', [*entry.keys()][0], auth="antoine")

            print(f'Table {tableName} has been deleted')
        
        clearDismanTable('mteObjectsTable')
        clearDismanTable('mteEventTable')
        clearDismanTable('mteTriggerTable')
    

    def activateAllEntries(self):

        def activateDismanTable(tableName):
            entryStatus = getTableColumns(self.snmpEngine.mibViewController, 'DISMAN-EVENT-MIB', tableName)[-1]
            controlColumn = self.snmpEngine.getTable('DISMAN-EVENT-MIB', tableName, entryStatus)[tableName]

            for entry in controlColumn:
                print("Activating entry...")
                self.snmpEngine.setByOID('active', [*entry.keys()][0], auth="antoine")

            print(f'Table {tableName} has been activated')
        
        activateDismanTable('mteObjectsTable')
        activateDismanTable('mteEventTable')
        activateDismanTable('mteTriggerTable')