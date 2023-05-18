from modules.devices.switch.switchTrapConfig import switchTrapConfig, mteTriggerTest
from modules.snmp import ManagedNode, Table, MibNode
from modules.utils import Entry


class Switch(ManagedNode):
    def __init__(self, ipAddress, credentials):
        ManagedNode.__init__(self, ipAddress, credentials=credentials)
        self.__name__ = 'Switch'

    
    ######################################################################################
    ################################ Trap control methods ################################
    ######################################################################################
    def resetTrapConfig(self):
        self._clearTrapConfig()
        self._setTrapConfig()
        self._activateTrapConfig()


    def getTriggers(self):
        triggers = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerTable').pullData('mteTriggerEnabled')
        indexes = [str(index[1]) for index in triggers.indexes]
        decoder = { 'true': 'On', 'false': 'Off' }
        return [f"{name} ({decoder[row[0]]})" for name, row in zip(indexes, triggers.values)], indexes


    def getEvents(self):
        events = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteEventTable').pullData('mteEventEnabled')
        indexes = [str(index[1]) for index in events.indexes]
        decoder = { 'true': 'On', 'false': 'Off' }
        return [f"{name} ({decoder[row[0]]})" for name, row in zip(indexes, events.values)], indexes


    def getTrigger(self, index):
        trigger = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerTable').pullData('mteTriggerComment', 'mteTriggerTest', 'mteTriggerSampleType', 'mteTriggerValueID', 'mteTriggerEnabled', startIndex=('antoine', index), maxRepetitions=1)
        return trigger, trigger.values[0][4] == 'true'
    
    
    def getEvent(self, index):
        event = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteEventTable').pullData('mteEventComment', 'mteEventEnabled', startIndex=('antoine', index), maxRepetitions=1)
        return event, event.values[0][1] == 'true'


    def enableTrigger(self, index):
        return MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteTriggerEnabled', 'antoine', index)).set('true', auth='antoine').ok


    def enableEvent(self, index):
        return MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteEventEnabled', 'antoine', index)).set('true', auth='antoine').ok


    def enableAuthenticationFailureTrap(self):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'snmpEnableAuthenTraps', 0)).set('enabled', auth='antoine').ok


    def disableTrigger(self, index):
        return MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteTriggerEnabled', 'antoine', index)).set('false', auth='antoine').ok


    def disableEvent(self, index):
        return MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteEventEnabled', 'antoine', index)).set('false', auth='antoine').ok


    def disableAuthenticationFailureTrap(self):
        return MibNode(self.snmpEngine, ('SNMPv2-MIB', 'snmpEnableAuthenTraps', 0)).set('disabled', auth='antoine').ok
    

    ######################################################################################
    ################################## Internal methods ##################################
    ######################################################################################
    def _setTrapConfig(self):

        def initDismanTable(tableName):
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', tableName)
            for entry in switchTrapConfig[tableName]:
                newRow = Entry(entry)
                newRow.resolve(self.snmpEngine)

                for index, varBinds in zip(newRow.indexes, newRow.args):
                    print('Creating new entry...')
                    if not table.setRow(index, varBinds, auth='antoine').ok:
                        print(f'Failed to create new entry in table {tableName}')

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
    

    def _clearTrapConfig(self):

        def clearDismanTable(tableName, controlColumn):
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', tableName)
            if table.setColumn(controlColumn, 'destroy', auth='antoine').ok:
                print(f'Table {tableName} has been deleted')
            else:
                print(f'Failed to delete table {tableName}')
        
        clearDismanTable('mteTriggerTable', 'mteTriggerEntryStatus')
        clearDismanTable('mteEventTable', 'mteEventEntryStatus')
        clearDismanTable('mteObjectsTable', 'mteObjectsEntryStatus')
    

    def _activateTrapConfig(self):

        def activateDismanTable(tableName, controlColumn):
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', tableName)
            if table.setColumn(controlColumn, 'active', auth='antoine').ok:
                print(f'Table {tableName} has been activated')
            else:
                print(f'Failed to activate table {tableName}')
        
        activateDismanTable('mteObjectsTable', 'mteObjectsEntryStatus')
        activateDismanTable('mteEventTable', 'mteEventEntryStatus')
        activateDismanTable('mteTriggerTable', 'mteTriggerEntryStatus')


    def _getTriggerTest(self, test, sampleType, index):
        if 'existence' in [test, mteTriggerTest[test]]:
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerExistenceTable')
            fullTestConfig = table.pullData('mteTriggerExistenceTest', 'mteTriggerExistenceEventOwner', 'mteTriggerExistenceEvent', startIndex=index, maxRepetitions=1)
            testConfig = {key: fullTestConfig[key] for key in ['mteTriggerExistenceTest']}
            eventIndex = [fullTestConfig['mteTriggerExistenceEventOwner'], fullTestConfig['mteTriggerExistenceEvent']]
        
        elif 'boolean' in [test, mteTriggerTest[test]]:
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerBooleanTable')
            fullTestConfig = table.pullData('mteTriggerBooleanComparison', 'mteTriggerBooleanValue', 'mteTriggerBooleanEventOwner', 'mteTriggerBooleanEvent', startIndex=index, maxRepetitions=1)
            testConfig = {key: fullTestConfig[key] for key in ['mteTriggerBooleanComparison', 'mteTriggerBooleanValue']}
            eventIndex = [fullTestConfig['mteTriggerBooleanEventOwner'], fullTestConfig['mteTriggerBooleanEvent']]
        
        elif 'threshold' in [test, mteTriggerTest[test]]:
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerThresholdTable')
            fullTestConfig = table.pullData('mteTriggerThresholdStartup', 'mteTriggerThresholdRising', 'mteTriggerThresholdFalling', 'mteTriggerThresholdDeltaRising', 'mteTriggerThresholdDeltaFalling', 'mteTriggerThresholdRisingEventOwner', 'mteTriggerThresholdRisingEvent', 'mteTriggerThresholdFallingEventOwner', 'mteTriggerThresholdFallingEvent', 'mteTriggerThresholdDeltaRisingEventOwner', 'mteTriggerThresholdDeltaRisingEvent', 'mteTriggerThresholdDeltaFallingEventOwner', 'mteTriggerThresholdDeltaFallingEvent', startIndex=index, maxRepetitions=1)
            
            if fullTestConfig['mteTriggerThresholdStartup'] == 'rising':

                if sampleType == 'absoluteValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdRising']}
                    eventIndex = [fullTestConfig['mteTriggerThresholdRisingEventOwner'], fullTestConfig['mteTriggerThresholdRisingEvent']]
                
                elif sampleType == 'deltaValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdDeltaRising']}
                    eventIndex = [fullTestConfig['mteTriggerThresholdDeltaRisingEventOwner'], fullTestConfig['mteTriggerThresholdDeltaRisingEvent']]
            
            elif fullTestConfig['mteTriggerThresholdStartup'] == 'falling':

                if sampleType == 'absoluteValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdFalling']}
                    eventIndex = [fullTestConfig['mteTriggerThresholdFallingEventOwner'], fullTestConfig['mteTriggerThresholdFallingEvent']]
                
                elif sampleType == 'deltaValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdDeltaFalling']}
                    eventIndex = [fullTestConfig['mteTriggerThresholdDeltaFallingEventOwner'], fullTestConfig['mteTriggerThresholdDeltaFallingEvent']]
            
            elif fullTestConfig['mteTriggerThresholdStartup'] == 'risingOrFalling':

                if sampleType == 'absoluteValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdRising', 'mteTriggerThresholdFalling']}
                    eventIndex = [[fullTestConfig['mteTriggerThresholdRisingEventOwner'], fullTestConfig['mteTriggerThresholdRisingEvent']],
                                    [fullTestConfig['mteTriggerThresholdFallingEventOwner'], fullTestConfig['mteTriggerThresholdFallingEvent']]]
                
                elif sampleType == 'deltaValue':
                    testConfig = {key: fullTestConfig[key] for key in ['mteTriggerThresholdStartup', 'mteTriggerThresholdDeltaRising', 'mteTriggerThresholdDeltaFalling']}
                    eventIndex = [[fullTestConfig['mteTriggerThresholdDeltaRisingEventOwner'], fullTestConfig['mteTriggerThresholdDeltaRisingEvent']],
                                    [fullTestConfig['mteTriggerThresholdDeltaFallingEventOwner'], fullTestConfig['mteTriggerThresholdDeltaFallingEvent']]]       
            
        return testConfig, eventIndex
    