from modules.devices.switch.switchTrapConfig import switchTrapConfig, mteTriggerTest
from modules.devices.switch.credentials import credentials
from modules.utils import Entry, getTableColumns
from modules.snmp import ManagedNode


class Switch(ManagedNode):
    def __init__(self, ipAddress):
        ManagedNode.__init__(self, ipAddress, credentials=credentials)


    ######################################################################################
    ################################ Information methods #################################
    ######################################################################################
    def getHealthMetrics(self, format='instSymbol.instIndex:valPretty'):
        healthMetrics = dict()
        # HOST-RESOURCES-MIB metrics
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemUptime', 0, format=format))
        healthMetrics.update(self.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0, format=format))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrStorageTable', 'hrStorageIndex', 'hrStorageUsed', format=format))
        healthMetrics.update(self.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrProcessorTable', 'hrProcessorFrwID', 'hrProcessorLoad', format=format))
        # IF-MIB metrics
        healthMetrics.update(self.snmpEngine.getTable('IF-MIB', 'ifTable', 'ifIndex', 'ifOperStatus', 'ifLastChange', format=format))
        return healthMetrics

    
    ######################################################################################
    ################################ Trap control methods ################################
    ######################################################################################
    def resetTrapConfig(self):
        self._clearTrapConfig()
        self._setTrapConfig()
        self._activateTrapConfig()


    def getTriggers(self, all=False):
        indexes = self.snmpEngine.walk('DISMAN-EVENT-MIB', 'mteTriggerEnabled', format='instIndex,valPretty')

        result = []
        for entry in indexes:
            index, enabled = entry[0]

            if all or bool(enabled):
                trigger, testConfig, eventConfig, _ = self.getTrigger(index)
                if all or eventConfig['event']['mteEventEnabled']:
                    result.append({'index': index,'trigger': trigger, 'testConfig': testConfig, 'eventConfig': eventConfig})

        return result


    def getEvents(self, all=True):
        indexes = self.snmpEngine.walk('DISMAN-EVENT-MIB', 'mteEventEnabled', format='instIndex,valPretty')

        result = []
        for entry in indexes:
            index, enabled = entry
            if all or bool(enabled):
                result.append(self.getEvent(index))

        return result


    def getTrigger(self, index):
        trigger = self.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', 'mteTriggerComment', 'mteTriggerTest', 'mteTriggerSampleType', 'mteTriggerValueID', 'mteTriggerEnabled', startIndex=index, maxRepetitions=1, format="instSymbol:valPretty")['mteTriggerTable'][0]
        testConfig, eventIndex = self._getTriggerTest(trigger['mteTriggerTest'], trigger['mteTriggerSampleType'], index)

        if isinstance(eventIndex[0], list):
            eventConfig = []
            for eventInd in eventIndex:
                eventConfig.append(self.getEvent(eventInd))
        else:
            eventConfig = self.getEvent(eventIndex)
        return trigger, testConfig, eventConfig, eventIndex

    
    def getEvent(self, index):
        return { 'index': index, 'event': self.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventTable', 'mteEventComment', 'mteEventEnabled', startIndex=index, maxRepetitions=1, format="instSymbol:valPretty")['mteEventTable'][0] }


    def enableTrigger(self, index):
        self.snmpEngine.set('true', 'DISMAN-EVENT-MIB', 'mteTriggerEnabled', *index, auth='antoine')
        _, _, eventConfig, eventIndex = self.getTrigger(index)
        if not eventConfig['mteEventEnabled']:
            self.enableEvent(eventIndex)


    def enableEvent(self, index):
        self.snmpEngine.set('true', 'DISMAN-EVENT-MIB', 'mteEventEnabled', *index, auth='antoine')


    def disableTrigger(self, index):
        self.snmpEngine.set('false', 'DISMAN-EVENT-MIB', 'mteTriggerEnabled', *index, auth='antoine')


    def disableEvent(self, index):
        self.snmpEngine.set('false', 'DISMAN-EVENT-MIB', 'mteEventEnabled', *index, auth='antoine')


    ######################################################################################
    ################################## Internal methods ##################################
    ######################################################################################
    def _setTrapConfig(self):

        def initDismanTable(tableName):
            for entry in switchTrapConfig[tableName]:
                newRow = Entry(entry)
                newRow.resolve(self.snmpEngine)

                for index, args in zip(newRow.indexes, newRow.args):
                    print('Creating new entry...')
                    newRow = self.snmpEngine.setTableRow('DISMAN-EVENT-MIB', index, *args, auth='antoine')
                    if not newRow: 
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

        def clearDismanTable(tableName):
            entryStatus = getTableColumns(self.snmpEngine.mibViewController, 'DISMAN-EVENT-MIB', tableName)[-1]
            controlColumn = self.snmpEngine.walk('DISMAN-EVENT-MIB', entryStatus, format='instOID:valOID')
            
            if not controlColumn:
                print(f"Table {tableName} is empty")
                return

            if isinstance(controlColumn, list):
                for instOid, in controlColumn:
                    print('Deleting entry...')
                    self.snmpEngine.setByOID('destroy', instOid, auth='antoine')
            else:
                instOid, = controlColumn
                self.snmpEngine.setByOID('destroy', instOid, auth='antoine')

            print(f'Table {tableName} has been deleted')
        
        clearDismanTable('mteObjectsTable')
        clearDismanTable('mteEventTable')
        clearDismanTable('mteTriggerTable')
    

    def _activateTrapConfig(self):

        def activateDismanTable(tableName):
            entryStatus = getTableColumns(self.snmpEngine.mibViewController, 'DISMAN-EVENT-MIB', tableName)[-1]
            controlColumn = self.snmpEngine.walk('DISMAN-EVENT-MIB', entryStatus, format='instOID:valOID')

            if not controlColumn:
                print(f"Table {tableName} is empty")
                return
             
            if isinstance(controlColumn, list):
                for instOid, in controlColumn:
                    print('Activating entry...')
                    self.snmpEngine.setByOID('active', instOid, auth='antoine')
            else:
                instOid, = controlColumn
                self.snmpEngine.setByOID('active', instOid, auth='antoine')

            print(f'Table {tableName} has been activated')
        
        activateDismanTable('mteObjectsTable')
        activateDismanTable('mteEventTable')
        activateDismanTable('mteTriggerTable')


    def _getTriggerTest(self, test, sampleType, index):
        if 'existence' in [test, mteTriggerTest[test]]:
            fullTestConfig = self.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerExistenceTable', 'mteTriggerExistenceTest', 'mteTriggerExistenceEventOwner', 'mteTriggerExistenceEvent', startIndex=index, maxRepetitions=1, format='instSymbol:valPretty')['mteTriggerExistenceTable'][0]
            testConfig = {key: fullTestConfig[key] for key in ['mteTriggerExistenceTest']}
            eventIndex = [fullTestConfig['mteTriggerExistenceEventOwner'], fullTestConfig['mteTriggerExistenceEvent']]
        
        elif 'boolean' in [test, mteTriggerTest[test]]:
            fullTestConfig = self.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerBooleanTable', 'mteTriggerBooleanComparison', 'mteTriggerBooleanValue', 'mteTriggerBooleanEventOwner', 'mteTriggerBooleanEvent', startIndex=index, maxRepetitions=1, format='instSymbol:valPretty')['mteTriggerBooleanTable'][0]
            testConfig = {key: fullTestConfig[key] for key in ['mteTriggerBooleanComparison', 'mteTriggerBooleanValue']}
            eventIndex = [fullTestConfig['mteTriggerBooleanEventOwner'], fullTestConfig['mteTriggerBooleanEvent']]
        
        elif 'threshold' in [test, mteTriggerTest[test]]:
            fullTestConfig = self.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerThresholdTable', 'mteTriggerThresholdStartup', 'mteTriggerThresholdRising', 'mteTriggerThresholdFalling', 'mteTriggerThresholdDeltaRising', 'mteTriggerThresholdDeltaFalling', 'mteTriggerThresholdRisingEventOwner', 'mteTriggerThresholdRisingEvent', 'mteTriggerThresholdFallingEventOwner', 'mteTriggerThresholdFallingEvent', 'mteTriggerThresholdDeltaRisingEventOwner', 'mteTriggerThresholdDeltaRisingEvent', 'mteTriggerThresholdDeltaFallingEventOwner', 'mteTriggerThresholdDeltaFallingEvent', startIndex=index, maxRepetitions=1, format='instSymbol:valPretty')['mteTriggerThresholdTable'][0]

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
    