from modules.devices.switch.switchTrapConfig import switchTrapConfig
from modules.devices.switch.credentials import switchCredentials
from modules.snmp import ManagedNode
from modules.utils import InstanceValue


class Switch(ManagedNode):
    def __init__(self, ipAddress):
        ManagedNode.__init__(self, ipAddress, credentials=switchCredentials)


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
                index, columns = entry['index'], entry['columns']
                args = [column_value for column_value in columns.items()]
                
                entryStatusColumn = [column for column in columns.keys() if "EntryStatus" in column]
                print("Checking for existing entry...")
                existingRow = self.snmpEngine.getTable('DISMAN-EVENT-MIB', tableName, *columns, startIndex=index.values(), maxRepetitions=1, format="valueOID")[tableName]
                
                if existingRow:

                    identical = True
                    existingRow = existingRow[0]
                    for column in columns:
                        if columns[column] != existingRow[column]:
                            identical = False
                            break
                        
                    if identical:
                        continue
                    else:
                        if len(entryStatusColumn) == 1:
                            print("Deleting old entry...")
                            self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', index.values(), (entryStatusColumn[0], 'destroy'), auth="antoine")
                
                for i, varBind in enumerate(args):
                    obj, val = varBind
                    if val and isinstance(val, InstanceValue):
                        args[i] = (obj, val.resolve(self.snmpEngine))

                print("Creating new entry...")
                newRow = self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', index.values(), *args, auth="antoine")
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
        