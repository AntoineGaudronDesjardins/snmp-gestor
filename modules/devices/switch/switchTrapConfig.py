##########################################################################################
##########################################################################################
############# Traps configuration file for the switch with DISMAN-EVENT-MIB ##############
##########################################################################################
##########################################################################################

from pysnmp.proto.rfc1902 import Bits
from modules.utils import createMibViewController, getOid
from modules.utils import Instance

# There is an issue with BITS value processing with pysnmp
mteEventActions = { 'notification': Bits('\x80'), 'set': Bits('\x40') }
mteTriggerTest = { 'existence': Bits('\x80'), 'boolean': Bits('\x40'), 'threshold': Bits('\x20') }
mteTriggerExistenceTest = { 'present': Bits('\x80'), 'absent': Bits('\x40'), 'changed': Bits('\x20') }
mteTriggerExistenceStartup = { 'present': Bits('\x80'), 'absent': Bits('\x40') }


##########################################################################################
##################################### OID resolution #####################################
##########################################################################################

mibViewController = createMibViewController()

# Monitored objects
sysUpTimeInstance = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'sysUpTimeInstance', stringify=True) # only for testing
hrProcessorLoad = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrProcessorLoad', stringify=True)
hrStorageUsed = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageUsed', stringify=True)
ifLastChange = getOid(mibViewController, 'IF-MIB', 'ifLastChange', stringify=True)

# Joined objects
hrSystemProcesses = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrSystemProcesses', 0, stringify=True)
hrProcessorFrwID = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrProcessorFrwID', stringify=True)
hrStorageIndex = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageIndex', stringify=True)
ifIndex = getOid(mibViewController, 'IF-MIB', 'ifIndex', stringify=True)
ifOperStatus = getOid(mibViewController, 'IF-MIB', 'ifOperStatus', stringify=True)

# Auxiliary objects
hrStorageSize = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageSize', stringify=True)

# Notification events
mteTriggerFired = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerFired', stringify=True)
mteTriggerRising = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerRising', stringify=True)
mteTriggerFalling = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerFired', stringify=True)


##########################################################################################
############################ Initial configuration definition ############################
##########################################################################################

switchTrapConfig = {
################################## Triggers definition ###################################
'mteTriggerTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteTriggerName': 'triggerName'
    #     },
    #     'columns': {
    #         'mteTriggerComment': 'comment...',
    #         'mteTriggerTest': mteTriggerTest['existence'] / mteTriggerTest['boolean'] / mteTriggerTest['threshold'],
    #         # create dependency to mteTriggerExistenceTable / mteTriggerBooleanTable / mteTriggerThresholdTable
    #         'mteTriggerSampleType': 'absoluteValue'/'deltaValue',
    #         # create dependency to mteTriggerDeltaTable
    #         'mteTriggerValueID': 'oid',
    #         'mteTriggerValueIDWildcard': 'true'/'false',
    #         'mteTriggerTargetTag': 'tag',
    #         'mteTriggerContextName': 'contextName',
    #         'mteTriggerContextNameWildcard': 'true'/'false',
    #         'mteTriggerFrequency': '10', # in seconds
    #         # create dependency to mteObjectsTable (tow next rows)
    #         'mteTriggerObjectsOwner': 'objectsOwner',
    #         'mteTriggerObjects': 'objects',
    #         'mteTriggerEnabled': 'true'/'false',
    #         'mteTriggerEntryStatus': 'active'/'notInService'/'notReady'/'createAndGo'/'createAndWait'/'destroy',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'TestTrigger'
        },
        'columns': {
            'mteTriggerComment': '',
            'mteTriggerTest': mteTriggerTest['boolean'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': sysUpTimeInstance,
            'mteTriggerValueIDWildcard': 'false',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '10', # in seconds
            'mteTriggerObjectsOwner': '',
            'mteTriggerObjects': '',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'MachineTooBusy'
        },
        'columns': {
            'mteTriggerComment': 'Warning: High Processor Load!',
            'mteTriggerTest': mteTriggerTest['boolean'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': hrProcessorLoad,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '10', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'processMetrics',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'MemoryUsageWarning'
        },
        'columns': {
            'mteTriggerComment': 'Warning: Memory usage has reached a critical level!',
            'mteTriggerTest': mteTriggerTest['threshold'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': Instance(hrStorageUsed, wildcarded=True, oidFlag=True),
            'mteTriggerValueIDWildcard': 'false',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '10', # in seconds
            'mteTriggerObjectsOwner': '',
            'mteTriggerObjects': '',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'InterfaceStatusUpdate'
        },
        'columns': {
            'mteTriggerComment': 'Warning: Interface state changed',
            'mteTriggerTest': mteTriggerTest['existence'],
            'mteTriggerSampleType': 'deltaValue',
            'mteTriggerValueID': ifLastChange,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '10', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'interfacesMetrics',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
],

############################ Configuration for delta sampling ############################
'mteTriggerDeltaTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteTriggerName': 'triggerName'
    #     },
    #     'columns': {
    #         'mteTriggerDeltaDiscontinuityID': 'oid',
    #         'mteTriggerDeltaDiscontinuityIDWildcard': 'true'/'false',
    #         'mteTriggerDeltaDiscontinuityIDType': 'timeTicks'/'timeStamp'/'dateAndTime',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'InterfaceStatusUpdate'
        },
        'columns': {
            'mteTriggerDeltaDiscontinuityID': sysUpTimeInstance,
            'mteTriggerDeltaDiscontinuityIDWildcard': 'false',
            'mteTriggerDeltaDiscontinuityIDType': 'timeTicks',
        },
    },
],

############################ Configuration for existence test ############################
'mteTriggerExistenceTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteTriggerName': 'triggerName'
    #     },
    #     'columns': {
    #         'mteTriggerExistenceTest': 'present'/'absent'/'changed',
    #         'mteTriggerExistenceStartup': 'present'/'absent',
    #         # create dependency to mteObjectsTable (tow next rows)
    #         'mteTriggerExistenceObjectsOwner': 'objectsOwner',
    #         'mteTriggerExistenceObjects': 'objects',
    #         # create dependency to mteEventTable (tow next rows)
    #         'mteTriggerExistenceEventOwner': 'eventOwner',
    #         'mteTriggerExistenceEvent': 'event',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'InterfaceStatusUpdate'
        },
        'columns': {
            'mteTriggerExistenceTest': mteTriggerExistenceTest['changed'],
            'mteTriggerExistenceStartup': mteTriggerExistenceStartup['present'],
            'mteTriggerExistenceObjectsOwner': '',
            'mteTriggerExistenceObjects': '',
            'mteTriggerExistenceEventOwner': 'antoine',
            'mteTriggerExistenceEvent': 'DeviceAlert',
        },
    },
],

############################# Configuration for boolean test #############################
'mteTriggerBooleanTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteTriggerName': 'triggerName'
    #     },
    #     'columns': {
    #         'mteTriggerBooleanComparison': 'unequal'/'equal'/'less'/'lessOrEqual'/'greater'/'greaterOrEqual',
    #         'mteTriggerBooleanValue': '20',
    #         'mteTriggerBooleanStartup': 'true'/'false',
    #         # create dependency to mteObjectsTable (tow next rows)
    #         'mteTriggerBooleanObjectsOwner': 'objectsOwner',
    #         'mteTriggerBooleanObjects': 'objects',
    #         # create dependency to mteEventTable (tow next rows)
    #         'mteTriggerBooleanEventOwner': 'eventOwner',
    #         'mteTriggerBooleanEvent': 'event',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'TestTrigger'
        },
        'columns': {
            'mteTriggerBooleanComparison': 'greaterOrEqual',
            'mteTriggerBooleanValue': '6000',
            'mteTriggerBooleanStartup': 'true',
            'mteTriggerBooleanObjectsOwner': '',
            'mteTriggerBooleanObjects': '',
            'mteTriggerBooleanEventOwner': 'antoine',
            'mteTriggerBooleanEvent': 'DeviceAlert',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'MachineTooBusy'
        },
        'columns': {
            'mteTriggerBooleanComparison': 'greaterOrEqual',
            'mteTriggerBooleanValue': '90',
            'mteTriggerBooleanStartup': 'true',
            'mteTriggerBooleanObjectsOwner': '',
            'mteTriggerBooleanObjects': '',
            'mteTriggerBooleanEventOwner': 'antoine',
            'mteTriggerBooleanEvent': 'DeviceAlert',
        },
    },
],

############################ Configuration for threshold test ############################
'mteTriggerThresholdTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteTriggerName': 'triggerName'
    #     },
    #     'columns': {
    #         'mteTriggerThresholdStartup': 'rising'/'falling'/'risingOrFalling',
    #         'mteTriggerThresholdRising': '20',
    #         'mteTriggerThresholdFalling': '10',
    #         'mteTriggerThresholdDeltaRising': '20',
    #         'mteTriggerThresholdDeltaFalling': '10',
    #         # create dependency to mteObjectsTable (tow next rows)
    #         'mteTriggerThresholdObjectsOwner': 'objectsOwner',
    #         'mteTriggerThresholdObjects': 'objects',
    #         # create dependency to mteEventTable (all next rows)
    #         'mteTriggerThresholdRisingEventOwner': 'risingEventOwner',
    #         'mteTriggerThresholdRisingEvent': 'risingEvent',
    #         'mteTriggerThresholdFallingEventOwner': 'fallingEventOwner',
    #         'mteTriggerThresholdFallingEvent': 'fallingEvent',
    #         'mteTriggerThresholdDeltaRisingEventOwner': 'deltaRisingEventOwner',
    #         'mteTriggerThresholdDeltaRisingEvent': 'deltaRisingEvent',
    #         'mteTriggerThresholdDeltaFallingEventOwner': 'deltaFallingEventOwner',
    #         'mteTriggerThresholdDeltaFallingEvent': 'deltaFallingEvent',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'MemoryUsageWarning'
        },
        'columns': {
            'mteTriggerThresholdStartup': 'rising',
            'mteTriggerThresholdRising': Instance(hrStorageSize, lambda x: int(0.9 * int(x)), wildcarded=True),
            'mteTriggerThresholdFalling': '0',
            'mteTriggerThresholdDeltaRising': '0',
            'mteTriggerThresholdDeltaFalling': '0',
            'mteTriggerThresholdObjectsOwner': '',
            'mteTriggerThresholdObjects': '',
            'mteTriggerThresholdRisingEventOwner': 'antoine',
            'mteTriggerThresholdRisingEvent': 'DeviceAlert',
            'mteTriggerThresholdFallingEventOwner': '',
            'mteTriggerThresholdFallingEvent': '',
            'mteTriggerThresholdDeltaRisingEventOwner': '',
            'mteTriggerThresholdDeltaRisingEvent': '',
            'mteTriggerThresholdDeltaFallingEventOwner': '',
            'mteTriggerThresholdDeltaFallingEvent': '',
        },
    },
],

############################### Objects groups definition ################################
'mteObjectsTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteObjectsName': 'objectsName',
    #         'mteObjectsIndex': 'arbitraryIndex'
    #     },
    #     'columns': {
    #         'mteObjectsID': 'oid',
    #         'mteObjectsIDWildcard': 'true'/'false',
    #         'mteObjectsEntryStatus': 'active'/'notInService'/'notReady'/'createAndGo'/'createAndWait'/'destroy',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'processMetrics',
            'mteObjectsIndex': '1'
        },
        'columns': {
            'mteObjectsID': hrSystemProcesses,
            'mteObjectsIDWildcard': 'false',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'processMetrics',
            'mteObjectsIndex': '2'
        },
        'columns': {
            'mteObjectsID': hrProcessorFrwID,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'processMetrics',
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': hrProcessorLoad,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'storageMetrics',
            'mteObjectsIndex': '1'
        },
        'columns': {
            'mteObjectsID': hrStorageIndex,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'storageMetrics',
            'mteObjectsIndex': '2'
        },
        'columns': {
            'mteObjectsID': hrStorageUsed,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'interfacesMetrics',
            'mteObjectsIndex': '1'
        },
        'columns': {
            'mteObjectsID': ifIndex,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'interfacesMetrics',
            'mteObjectsIndex': '2'
        },
        'columns': {
            'mteObjectsID': ifOperStatus,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
],

################################### Events definition ####################################
'mteEventTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteEventName': 'eventName'
    #     },
    #     'columns': {
    #         'mteEventComment': 'comment...',
    #         # create dependency to mteEventNotificationTable / mteEventSetTable
    #         'mteEventActions': mteEventActions['notification'] / mteEventActions['set'],
    #         'mteEventEnabled': 'true'/'false',
    #         'mteEventEntryStatus': 'active'/'notInService'/'notReady'/'createAndGo'/'createAndWait'/'destroy',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'DeviceAlert'
        },
        'columns': {
            'mteEventComment': '',
            'mteEventActions': mteEventActions['notification'],
            'mteEventEnabled': 'true',
            'mteEventEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
],

######################### Configuration for notification events ##########################
'mteEventNotificationTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteEventName': 'eventName'
    #     },
    #     'columns': {
    #         'mteEventNotification': 'notificationOid',
    #         # create dependency to mteObjectsTable (tow next rows)
    #         'mteEventNotificationObjectsOwner': 'objectsOwner',
    #         'mteEventNotificationObjects': 'objects',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'DeviceAlert'
        },
        'columns': {
            'mteEventNotification': mteTriggerFired,
            'mteEventNotificationObjectsOwner': '',
            'mteEventNotificationObjects': '',
        },
    },
],

############################# Configuration for set events ###############################
'mteEventSetTable': [
    # # This first entry is a template for the next ones
    # {
    #     'index': {
    #         'mteOwner': 'owner',
    #         'mteEventName': 'eventName'
    #     },
    #     'columns': {
    #         'mteEventSetObject': 'oid',
    #         'mteEventSetObjectWildcard': 'true'/'false',
    #         'mteEventSetValue': 'value',
    #         'mteEventSetTargetTag': 'tag',
    #         'mteEventSetContextName': 'contextName',
    #         'mteEventSetContextNameWildcard': 'true'/'false',
    #     },
    # },
]}


##########################################################################################
################################## Notification Objects ##################################
##########################################################################################
# mteTriggerFired : Notification that the trigger indicated by the object instances has 
#                   fired, for triggers with mteTriggerType 'boolean' or 'existence'.
#
# mteTriggerRising : Notification that the rising threshold was met for triggers with
#                    mteTriggerType 'threshold'.
#
# mteTriggerFalling : Notification that the falling threshold was met for triggers with 
#                     mteTriggerType 'threshold'.
#
# mteTriggerFailure : Notification that an attempt to check a trigger has failed. The 
#                     network manager must enable this notification only with a certain
#                     fear and trembling, as it can easily crowd out more important
#                     information. It should be used only to help diagnose a problem that
#                     has appeared in the error counters and can not be found otherwise.
#
# mteEventSetFailure : Notification that an attempt to do a set in response to an event
#                      has failed. The network manager must enable this notification only
#                      with a certain fear and trembling, as it can easily crowd out more
#                      important information. It should be used only to help diagnose a
#                      problem that has appeared in the error counters and can not be
#                      found otherwise.
#