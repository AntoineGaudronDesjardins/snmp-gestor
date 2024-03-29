##########################################################################################
##########################################################################################
############# Traps configuration file for the switch with DISMAN-EVENT-MIB ##############
##########################################################################################
##########################################################################################

from modules.utils import createMibViewController, getOid
from modules.utils import Instance, NamedBits

# There is an issue with BITS value processing with pysnmp    
mteEventActions = NamedBits({'notification': 0, 'set': 1})
mteTriggerTest = NamedBits({'existence': 0, 'boolean': 1, 'threshold': 2})
mteTriggerExistenceTest = NamedBits({'present': 0, 'absent': 1, 'changed': 2})
mteTriggerExistenceStartup = NamedBits({'present': 0, 'absent': 1})


##########################################################################################
##################################### OID resolution #####################################
##########################################################################################

mibViewController = createMibViewController()

# Monitored objects
hrProcessorLoad = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrProcessorLoad')
hrStorageUsed = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageUsed')
ifLastChange = getOid(mibViewController, 'IF-MIB', 'ifLastChange')

# Triggers descr
# mteTriggerComment = {
#     'MachineTooBusy': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'MachineTooBusy'),
#     'MemoryUsageWarning': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'MemoryUsageWarning'),
#     'InterfaceStatusUpdate': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'InterfaceStatusUpdate'),
#     'IncommingTrafficOverload': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'IncommingTrafficOverload'),
#     'UnusualOutgoingTraffic': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'UnusualOutgoingTraffic'),
#     'PerformanceIssue': getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerComment', 'antoine', 'PerformanceIssue'),
# }

# Joined objects
hrSystemProcesses = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrSystemProcesses', 0)
hrProcessorFrwID = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrProcessorFrwID')
hrStorageIndex = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageIndex')
hrStorageDescr = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageDescr')
ifIndex = getOid(mibViewController, 'IF-MIB', 'ifIndex')
ifDescr = getOid(mibViewController, 'IF-MIB', 'ifDescr')
ifOperStatus = getOid(mibViewController, 'IF-MIB', 'ifOperStatus')
ifInOctets = getOid(mibViewController, 'IF-MIB', 'ifInOctets')
ifInUcastPkts = getOid(mibViewController, 'IF-MIB', 'ifInUcastPkts')
ifInNUcastPkts = getOid(mibViewController, 'IF-MIB', 'ifInNUcastPkts')
ifInUnknownProtos = getOid(mibViewController, 'IF-MIB', 'ifInUnknownProtos')
ifOutOctets = getOid(mibViewController, 'IF-MIB', 'ifOutOctets')
ifOutUcastPkts = getOid(mibViewController, 'IF-MIB', 'ifOutUcastPkts')
ifOutNUcastPkts = getOid(mibViewController, 'IF-MIB', 'ifOutNUcastPkts')
ifInDiscards = getOid(mibViewController, 'IF-MIB', 'ifInDiscards')
ifOutDiscards = getOid(mibViewController, 'IF-MIB', 'ifOutDiscards')
ipIfStatsInHdrErrors = getOid(mibViewController, 'IP-MIB', 'ipIfStatsInHdrErrors')
ipIfStatsInNoRoutes = getOid(mibViewController, 'IP-MIB', 'ipIfStatsInNoRoutes')
ipIfStatsInAddrErrors = getOid(mibViewController, 'IP-MIB', 'ipIfStatsInAddrErrors')
udpInErrors = getOid(mibViewController, 'UDP-MIB', 'udpInErrors')
tcpInErrs = getOid(mibViewController, 'TCP-MIB', 'tcpInErrs')
snmpInBadVersions = getOid(mibViewController, 'SNMPv2-MIB', 'snmpInBadVersions', 0)
snmpInBadCommunityNames = getOid(mibViewController, 'SNMPv2-MIB', 'snmpInBadCommunityNames', 0)
snmpInBadCommunityUses = getOid(mibViewController, 'SNMPv2-MIB', 'snmpInBadCommunityUses', 0)
snmpInASNParseErrs = getOid(mibViewController, 'SNMPv2-MIB', 'snmpInASNParseErrs', 0)

# Auxiliary objects
sysUpTimeInstance = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'sysUpTimeInstance')
hrStorageSize = getOid(mibViewController, 'HOST-RESOURCES-MIB', 'hrStorageSize')

# Notification events
mteTriggerFired = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerFired')
mteTriggerRising = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerRising')
mteTriggerFalling = getOid(mibViewController, 'DISMAN-EVENT-MIB', 'mteTriggerFired')


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
            'mteTriggerName': 'MachineTooBusy'
        },
        'columns': {
            'mteTriggerComment': 'Trigger when the mean time of the CPU ocupation on one minute reach 90%.',
            'mteTriggerTest': mteTriggerTest['boolean'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': hrProcessorLoad,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
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
            'mteTriggerComment': 'Trigger when memory usage reach 90% of the maximal size. This trigger is replicate for each memory unit of the device',
            'mteTriggerTest': mteTriggerTest['threshold'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': Instance(hrStorageUsed, wildcarded=True, oidFlag=True),
            'mteTriggerValueIDWildcard': 'false',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
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
            'mteTriggerComment': 'Trigger when an interface of the device knows a change of state.',
            'mteTriggerTest': mteTriggerTest['existence'],
            'mteTriggerSampleType': 'deltaValue',
            'mteTriggerValueID': ifLastChange,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'interfacesMetrics',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'IncommingTrafficOverload'
        },
        'columns': {
            'mteTriggerComment': 'Trigger when the incomming number of octets rises.',
            'mteTriggerTest': mteTriggerTest['boolean'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': ifInOctets,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'incommingTrafficMetrics',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'UnusualOutgoingTraffic'
        },
        'columns': {
            'mteTriggerComment': 'Trigger when the outgoing octets cross over given thresholds.',
            'mteTriggerTest': mteTriggerTest['threshold'],
            'mteTriggerSampleType': 'absoluteValue',
            'mteTriggerValueID': ifOutOctets,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'outgoingTrafficMetrics',
            'mteTriggerEnabled': 'true',
            'mteTriggerEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'PerformanceIssue'
        },
        'columns': {
            'mteTriggerComment': 'Trigger when the variation of the number of droped packets reach limit threshold.',
            'mteTriggerTest': mteTriggerTest['boolean'],
            'mteTriggerSampleType': 'deltaValue',
            'mteTriggerValueID': ifOutDiscards,
            'mteTriggerValueIDWildcard': 'true',
            'mteTriggerTargetTag': '',
            'mteTriggerContextName': '',
            'mteTriggerContextNameWildcard': 'false',
            'mteTriggerFrequency': '5', # in seconds
            'mteTriggerObjectsOwner': 'antoine',
            'mteTriggerObjects': 'errorsTrafficMetrics',
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
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'PerformanceIssue'
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
            'mteTriggerName': 'MachineTooBusy'
        },
        'columns': {
            'mteTriggerBooleanComparison': 'greaterOrEqual',
            'mteTriggerBooleanValue': '90',
            'mteTriggerBooleanStartup': 'false',
            'mteTriggerBooleanObjectsOwner': '',
            'mteTriggerBooleanObjects': '',
            'mteTriggerBooleanEventOwner': 'antoine',
            'mteTriggerBooleanEvent': 'DeviceAlert',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'IncommingTrafficOverload'
        },
        'columns': {
            'mteTriggerBooleanComparison': 'greaterOrEqual',
            'mteTriggerBooleanValue': '1000000',
            'mteTriggerBooleanStartup': 'false',
            'mteTriggerBooleanObjectsOwner': '',
            'mteTriggerBooleanObjects': '',
            'mteTriggerBooleanEventOwner': 'antoine',
            'mteTriggerBooleanEvent': 'TrafficAlert',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'PerformanceIssue'
        },
        'columns': {
            'mteTriggerBooleanComparison': 'greaterOrEqual',
            'mteTriggerBooleanValue': '5',
            'mteTriggerBooleanStartup': 'false',
            'mteTriggerBooleanObjectsOwner': '',
            'mteTriggerBooleanObjects': '',
            'mteTriggerBooleanEventOwner': 'antoine',
            'mteTriggerBooleanEvent': 'PerformanceAlert',
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
    {
        'index': {
            'mteOwner': 'antoine',
            'mteTriggerName': 'UnusualOutgoingTraffic'
        },
        'columns': {
            'mteTriggerThresholdStartup': 'rising',
            'mteTriggerThresholdRising': '1000000',
            'mteTriggerThresholdFalling': '0',
            'mteTriggerThresholdDeltaRising': '1000000',
            'mteTriggerThresholdDeltaFalling': '0',
            'mteTriggerThresholdObjectsOwner': '',
            'mteTriggerThresholdObjects': '',
            'mteTriggerThresholdRisingEventOwner': '',
            'mteTriggerThresholdRisingEvent': '',
            'mteTriggerThresholdFallingEventOwner': '',
            'mteTriggerThresholdFallingEvent': '',
            'mteTriggerThresholdDeltaRisingEventOwner': 'antoine',
            'mteTriggerThresholdDeltaRisingEvent': 'TrafficAlert',
            'mteTriggerThresholdDeltaFallingEventOwner': 'antoine',
            'mteTriggerThresholdDeltaFallingEvent': 'TrafficAlert',
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
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'processMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['MachineTooBusy'],
    #         'mteObjectsIDWildcard': 'false',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'processMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsIndex': '3'
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
            'mteObjectsIndex': '4'
        },
        'columns': {
            'mteObjectsID': hrProcessorLoad,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'storageMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['MemoryUsageWarning'],
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'storageMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': hrStorageDescr,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'storageMetrics',
            'mteObjectsIndex': '4'
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
            'mteObjectsName': 'storageMetrics',
            'mteObjectsIndex': '5'
        },
        'columns': {
            'mteObjectsID': hrStorageSize,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'interfacesMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['InterfaceStatusUpdate'],
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'interfacesMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': ifOperStatus,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'interfacesMetrics',
            'mteObjectsIndex': '4'
        },
        'columns': {
            'mteObjectsID': ifDescr,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'incommingTrafficMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['IncommingTrafficOverload'],
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'incommingTrafficMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsName': 'incommingTrafficMetrics',
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': ifInOctets,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'incommingTrafficMetrics',
            'mteObjectsIndex': '4'
        },
        'columns': {
            'mteObjectsID': ifInUcastPkts,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'incommingTrafficMetrics',
            'mteObjectsIndex': '5'
        },
        'columns': {
            'mteObjectsID': ifInNUcastPkts,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'incommingTrafficMetrics',
            'mteObjectsIndex': '6'
        },
        'columns': {
            'mteObjectsID': ifInUnknownProtos,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'outgoingTrafficMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['UnusualOutgoingTraffic'],
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'outgoingTrafficMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsName': 'outgoingTrafficMetrics',
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': ifOutOctets,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'outgoingTrafficMetrics',
            'mteObjectsIndex': '4'
        },
        'columns': {
            'mteObjectsID': ifOutUcastPkts,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'outgoingTrafficMetrics',
            'mteObjectsIndex': '5'
        },
        'columns': {
            'mteObjectsID': ifOutNUcastPkts,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'errorsTrafficMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': mteTriggerComment['PerformanceIssue'],
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'errorsTrafficMetrics',
            'mteObjectsIndex': '2'
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
            'mteObjectsName': 'errorsTrafficMetrics',
            'mteObjectsIndex': '3'
        },
        'columns': {
            'mteObjectsID': ifInDiscards,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteObjectsName': 'errorsTrafficMetrics',
            'mteObjectsIndex': '4'
        },
        'columns': {
            'mteObjectsID': ifOutDiscards,
            'mteObjectsIDWildcard': 'true',
            'mteObjectsEntryStatus': 'createAndGo',
        },
    },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'intrusionMetrics',
    #         'mteObjectsIndex': '1'
    #     },
    #     'columns': {
    #         'mteObjectsID': snmpInBadVersions,
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'intrusionMetrics',
    #         'mteObjectsIndex': '2'
    #     },
    #     'columns': {
    #         'mteObjectsID': snmpInBadCommunityNames,
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'intrusionMetrics',
    #         'mteObjectsIndex': '3'
    #     },
    #     'columns': {
    #         'mteObjectsID': snmpInBadCommunityUses,
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
    # {
    #     'index': {
    #         'mteOwner': 'antoine',
    #         'mteObjectsName': 'intrusionMetrics',
    #         'mteObjectsIndex': '4'
    #     },
    #     'columns': {
    #         'mteObjectsID': snmpInASNParseErrs,
    #         'mteObjectsIDWildcard': 'true',
    #         'mteObjectsEntryStatus': 'createAndGo',
    #     },
    # },
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
            'mteEventComment': 'Device related issue',
            'mteEventActions': mteEventActions['notification'],
            'mteEventEnabled': 'true',
            'mteEventEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'TrafficAlert'
        },
        'columns': {
            'mteEventComment': 'Anormal traffic load',
            'mteEventActions': mteEventActions['notification'],
            'mteEventEnabled': 'true',
            'mteEventEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'PerformanceAlert'
        },
        'columns': {
            'mteEventComment': 'Performance issue',
            'mteEventActions': mteEventActions['notification'],
            'mteEventEnabled': 'true',
            'mteEventEntryStatus': 'createAndWait', # Once dependencies created, set to 'active'
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'IntrusionAlert'
        },
        'columns': {
            'mteEventComment': 'Unauthorized activity',
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
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'TrafficAlert'
        },
        'columns': {
            'mteEventNotification': mteTriggerFired,
            'mteEventNotificationObjectsOwner': '',
            'mteEventNotificationObjects': '',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'PerformanceAlert'
        },
        'columns': {
            'mteEventNotification': mteTriggerFired,
            'mteEventNotificationObjectsOwner': '',
            'mteEventNotificationObjects': '',
        },
    },
    {
        'index': {
            'mteOwner': 'antoine',
            'mteEventName': 'IntrusionAlert'
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