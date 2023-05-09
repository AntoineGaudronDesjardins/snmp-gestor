from modules.devices.switch.switchTrapConfig import switchTrapConfig, mteTriggerTest
from modules.snmp import ManagedNode, Table, MibNode
from modules.utils import Entry
from conf import switchCredentials


class Switch(ManagedNode):
    def __init__(self, ipAddress):
        ManagedNode.__init__(self, ipAddress, credentials=switchCredentials)


    ######################################################################################
    ################################ Information methods #################################
    ######################################################################################
    def getHealthMetrics(self):
        healthMetrics = []
        # HOST-RESOURCES-MIB metrics
        healthMetrics.append(MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemUptime', 0)).get())
        healthMetrics.append(MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemProcesses', 0)).get())
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrStorageTable').pullData('hrStorageIndex', 'hrStorageUsed'))
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrProcessorTable').pullData('hrProcessorFrwID', 'hrProcessorLoad'))
        # IF-MIB metrics
        healthMetrics.append(Table(self.snmpEngine, 'IF-MIB', 'ifTable').pullData('ifIndex', 'ifOperStatus', 'ifLastChange'))
        return healthMetrics

    
    ######################################################################################
    ################################ Trap control methods ################################
    ######################################################################################
    def resetTrapConfig(self):
        self._clearTrapConfig()
        self._setTrapConfig()
        self._activateTrapConfig()


    def getTriggers(self, all=False):
        return Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerTable').pullData('mteTriggerComment', 'mteTriggerTest', 'mteTriggerSampleType', 'mteTriggerValueID', 'mteTriggerEnabled')


    def getEvents(self, all=True):
        return Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteEventTable').pullData('mteEventComment', 'mteEventEnabled')


    def getTrigger(self, index):
        return Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteTriggerTable').pullData('mteTriggerComment', 'mteTriggerTest', 'mteTriggerSampleType', 'mteTriggerValueID', 'mteTriggerEnabled', startIndex=index, maxRepetitions=1)
    
    
    def getEvent(self, index):
        return Table(self.snmpEngine, 'DISMAN-EVENT-MIB', 'mteEventTable').pullData('mteEventComment', 'mteEventEnabled', startIndex=index, maxRepetitions=1)


    def enableTrigger(self, index):
        MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteTriggerEnabled', index)).set('true', auth='antoine')


    def enableEvent(self, index):
        MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteEventEnabled', *index)).set('true', auth='antoine')
    

    def enableAuthenticationFailureTrap(self):
        MibNode(self.snmpEngine, ('SNMPv2-MIB', 'snmpEnableAuthenTraps', 0)).set('enabled', auth='antoine')


    def disableTrigger(self, index):
        MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteTriggerEnabled', *index)).set('false', auth='antoine')


    def disableEvent(self, index):
        MibNode(self.snmpEngine, ('DISMAN-EVENT-MIB', 'mteEventEnabled', *index)).set('false', auth='antoine')
    

    def disableAuthenticationFailureTrap(self):
        MibNode(self.snmpEngine, ('SNMPv2-MIB', 'snmpEnableAuthenTraps', 0)).set('disabled', auth='antoine')


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
                    newRow = table.setRow(index, varBinds, auth='antoine')
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

        def clearDismanTable(tableName, controlColumn):
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', tableName)
            table.setColumn(controlColumn, 'destroy', auth='antoine')
            print(f'Table {tableName} has been deleted')
        
        clearDismanTable('mteTriggerTable', 'mteTriggerEntryStatus')
        clearDismanTable('mteEventTable', 'mteEventEntryStatus')
        clearDismanTable('mteObjectsTable', 'mteObjectsEntryStatus')
    

    def _activateTrapConfig(self):

        def activateDismanTable(tableName, controlColumn):
            table = Table(self.snmpEngine, 'DISMAN-EVENT-MIB', tableName)
            table.setColumn(controlColumn, 'active', auth='antoine')
            print(f'Table {tableName} has been activated')
        
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
    