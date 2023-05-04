#
# PySNMP MIB module NOTIFICATION-LOG-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://C:\Users\antoi\OneDrive - CentraleSupelec\ETSI\gestion_de_redes\proyecto\pythonScripts\mibs\mibs\NOTIFICATION-LOG-MIB.mib
# Produced by pysmi-0.3.4 at Mon Apr 24 01:14:58 2023
# On host ? platform ? version ? by user ?
# Using Python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]
#
ObjectIdentifier, OctetString, Integer = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint")
SnmpAdminString, SnmpEngineID = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString", "SnmpEngineID")
NotificationGroup, ObjectGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ObjectGroup", "ModuleCompliance")
iso, TimeTicks, IpAddress, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Opaque, ObjectIdentity, NotificationType, Integer32, Counter64, Gauge32, Counter32, Unsigned32, MibIdentifier, mib_2, Bits = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "TimeTicks", "IpAddress", "ModuleIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Opaque", "ObjectIdentity", "NotificationType", "Integer32", "Counter64", "Gauge32", "Counter32", "Unsigned32", "MibIdentifier", "mib-2", "Bits")
TextualConvention, RowStatus, TAddress, DateAndTime, DisplayString, StorageType, TDomain, TimeStamp = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "RowStatus", "TAddress", "DateAndTime", "DisplayString", "StorageType", "TDomain", "TimeStamp")
notificationLogMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 92))
notificationLogMIB.setRevisions(('2000-11-27 00:00',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: notificationLogMIB.setRevisionsDescriptions(('This is the initial version of this MIB. Published as RFC 3014',))
if mibBuilder.loadTexts: notificationLogMIB.setLastUpdated('200011270000Z')
if mibBuilder.loadTexts: notificationLogMIB.setOrganization('IETF Distributed Management Working Group')
if mibBuilder.loadTexts: notificationLogMIB.setContactInfo('Ramanathan Kavasseri Cisco Systems, Inc. 170 West Tasman Drive, San Jose CA 95134-1706. Phone: +1 408 527 2446 Email: ramk@cisco.com')
if mibBuilder.loadTexts: notificationLogMIB.setDescription('The MIB module for logging SNMP Notifications, that is, Traps and Informs.')
notificationLogMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1))
nlmConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 1))
nlmStats = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 2))
nlmLog = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 3))
nlmConfigGlobalEntryLimit = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 1, 1), Unsigned32()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: nlmConfigGlobalEntryLimit.setStatus('current')
if mibBuilder.loadTexts: nlmConfigGlobalEntryLimit.setDescription('The maximum number of notification entries that may be held in nlmLogTable for all nlmLogNames added together. A particular setting does not guarantee that much data can be held. If an application changes the limit while there are Notifications in the log, the oldest Notifications MUST be discarded to bring the log down to the new limit - thus the value of nlmConfigGlobalEntryLimit MUST take precedence over the values of nlmConfigGlobalAgeOut and nlmConfigLogEntryLimit, even if the Notification being discarded has been present for fewer minutes than the value of nlmConfigGlobalAgeOut, or if the named log has fewer entries than that specified in nlmConfigLogEntryLimit. A value of 0 means no limit. Please be aware that contention between multiple managers trying to set this object to different values MAY affect the reliability and completeness of data seen by each manager.')
nlmConfigGlobalAgeOut = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 1, 2), Unsigned32().clone(1440)).setUnits('minutes').setMaxAccess("readwrite")
if mibBuilder.loadTexts: nlmConfigGlobalAgeOut.setStatus('current')
if mibBuilder.loadTexts: nlmConfigGlobalAgeOut.setDescription('The number of minutes a Notification SHOULD be kept in a log before it is automatically removed. If an application changes the value of nlmConfigGlobalAgeOut, Notifications older than the new time MAY be discarded to meet the new time. A value of 0 means no age out. Please be aware that contention between multiple managers trying to set this object to different values MAY affect the reliability and completeness of data seen by each manager.')
nlmConfigLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 1, 3), )
if mibBuilder.loadTexts: nlmConfigLogTable.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogTable.setDescription('A table of logging control entries.')
nlmConfigLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1), ).setIndexNames((0, "NOTIFICATION-LOG-MIB", "nlmLogName"))
if mibBuilder.loadTexts: nlmConfigLogEntry.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogEntry.setDescription("A logging control entry. Depending on the entry's storage type entries may be supplied by the system or created and deleted by applications using nlmConfigLogEntryStatus.")
nlmLogName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)))
if mibBuilder.loadTexts: nlmLogName.setStatus('current')
if mibBuilder.loadTexts: nlmLogName.setDescription('The name of the log. An implementation may allow multiple named logs, up to some implementation-specific limit (which may be none). A zero-length log name is reserved for creation and deletion by the managed system, and MUST be used as the default log name by systems that do not support named logs.')
nlmConfigLogFilterName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)).clone(hexValue="")).setMaxAccess("readcreate")
if mibBuilder.loadTexts: nlmConfigLogFilterName.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogFilterName.setDescription('A value of snmpNotifyFilterProfileName as used as an index into the snmpNotifyFilterTable in the SNMP Notification MIB, specifying the locally or remotely originated Notifications to be filtered out and not logged in this log. A zero-length value or a name that does not identify an existing entry in snmpNotifyFilterTable indicate no Notifications are to be logged in this log.')
nlmConfigLogEntryLimit = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 3), Unsigned32()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: nlmConfigLogEntryLimit.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogEntryLimit.setDescription('The maximum number of notification entries that can be held in nlmLogTable for this named log. A particular setting does not guarantee that that much data can be held. If an application changes the limit while there are Notifications in the log, the oldest Notifications are discarded to bring the log down to the new limit. A value of 0 indicates no limit. Please be aware that contention between multiple managers trying to set this object to different values MAY affect the reliability and completeness of data seen by each manager.')
nlmConfigLogAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(("enabled", 1), ("disabled", 2))).clone('enabled')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: nlmConfigLogAdminStatus.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogAdminStatus.setDescription("Control to enable or disable the log without otherwise disturbing the log's entry. Please be aware that contention between multiple managers trying to set this object to different values MAY affect the reliability and completeness of data seen by each manager.")
nlmConfigLogOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(("disabled", 1), ("operational", 2), ("noFilter", 3)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmConfigLogOperStatus.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogOperStatus.setDescription('The operational status of this log: disabled administratively disabled operational administratively enabled and working noFilter administratively enabled but either nlmConfigLogFilterName is zero length or does not name an existing entry in snmpNotifyFilterTable')
nlmConfigLogStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 6), StorageType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: nlmConfigLogStorageType.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogStorageType.setDescription('The storage type of this conceptual row.')
nlmConfigLogEntryStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 7), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: nlmConfigLogEntryStatus.setStatus('current')
if mibBuilder.loadTexts: nlmConfigLogEntryStatus.setDescription("Control for creating and deleting entries. Entries may be modified while active. For non-null-named logs, the managed system records the security credentials from the request that sets nlmConfigLogStatus to 'active' and uses that identity to apply access control to the objects in the Notification to decide if that Notification may be logged.")
nlmStatsGlobalNotificationsLogged = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 2, 1), Counter32()).setUnits('notifications').setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmStatsGlobalNotificationsLogged.setStatus('current')
if mibBuilder.loadTexts: nlmStatsGlobalNotificationsLogged.setDescription('The number of Notifications put into the nlmLogTable. This counts a Notification once for each log entry, so a Notification put into multiple logs is counted multiple times.')
nlmStatsGlobalNotificationsBumped = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 2, 2), Counter32()).setUnits('notifications').setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmStatsGlobalNotificationsBumped.setStatus('current')
if mibBuilder.loadTexts: nlmStatsGlobalNotificationsBumped.setDescription('The number of log entries discarded to make room for a new entry due to lack of resources or the value of nlmConfigGlobalEntryLimit or nlmConfigLogEntryLimit. This does not include entries discarded due to the value of nlmConfigGlobalAgeOut.')
nlmStatsLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 2, 3), )
if mibBuilder.loadTexts: nlmStatsLogTable.setStatus('current')
if mibBuilder.loadTexts: nlmStatsLogTable.setDescription('A table of Notification log statistics entries.')
nlmStatsLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1), )
nlmConfigLogEntry.registerAugmentions(("NOTIFICATION-LOG-MIB", "nlmStatsLogEntry"))
nlmStatsLogEntry.setIndexNames(*nlmConfigLogEntry.getIndexNames())
if mibBuilder.loadTexts: nlmStatsLogEntry.setStatus('current')
if mibBuilder.loadTexts: nlmStatsLogEntry.setDescription('A Notification log statistics entry.')
nlmStatsLogNotificationsLogged = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1, 1), Counter32()).setUnits('notifications').setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmStatsLogNotificationsLogged.setStatus('current')
if mibBuilder.loadTexts: nlmStatsLogNotificationsLogged.setDescription('The number of Notifications put in this named log.')
nlmStatsLogNotificationsBumped = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1, 2), Counter32()).setUnits('notifications').setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmStatsLogNotificationsBumped.setStatus('current')
if mibBuilder.loadTexts: nlmStatsLogNotificationsBumped.setDescription('The number of log entries discarded from this named log to make room for a new entry due to lack of resources or the value of nlmConfigGlobalEntryLimit or nlmConfigLogEntryLimit. This does not include entries discarded due to the value of nlmConfigGlobalAgeOut.')
nlmLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 3, 1), )
if mibBuilder.loadTexts: nlmLogTable.setStatus('current')
if mibBuilder.loadTexts: nlmLogTable.setDescription('A table of Notification log entries. It is an implementation-specific matter whether entries in this table are preserved across initializations of the management system. In general one would expect that they are not. Note that keeping entries across initializations of the management system leads to some confusion with counters and TimeStamps, since both of those are based on sysUpTime, which resets on management initialization. In this situation, counters apply only after the reset and nlmLogTime for entries made before the reset MUST be set to 0.')
nlmLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1), ).setIndexNames((0, "NOTIFICATION-LOG-MIB", "nlmLogName"), (0, "NOTIFICATION-LOG-MIB", "nlmLogIndex"))
if mibBuilder.loadTexts: nlmLogEntry.setStatus('current')
if mibBuilder.loadTexts: nlmLogEntry.setDescription('A Notification log entry. Entries appear in this table when Notifications occur and pass filtering by nlmConfigLogFilterName and access control. They are removed to make way for new entries due to lack of resources or the values of nlmConfigGlobalEntryLimit, nlmConfigGlobalAgeOut, or nlmConfigLogEntryLimit. If adding an entry would exceed nlmConfigGlobalEntryLimit or system resources in general, the oldest entry in any log SHOULD be removed to make room for the new one. If adding an entry would exceed nlmConfigLogEntryLimit the oldest entry in that log SHOULD be removed to make room for the new one. Before the managed system puts a locally-generated Notification into a non-null-named log it assures that the creator of the log has access to the information in the Notification. If not it does not log that Notification in that log.')
nlmLogIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts: nlmLogIndex.setStatus('current')
if mibBuilder.loadTexts: nlmLogIndex.setDescription('A monotonically increasing integer for the sole purpose of indexing entries within the named log. When it reaches the maximum value, an extremely unlikely event, the agent wraps the value back to 1.')
nlmLogTime = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 2), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogTime.setStatus('current')
if mibBuilder.loadTexts: nlmLogTime.setDescription('The value of sysUpTime when the entry was placed in the log. If the entry occurred before the most recent management system initialization this object value MUST be set to zero.')
nlmLogDateAndTime = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 3), DateAndTime()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogDateAndTime.setStatus('current')
if mibBuilder.loadTexts: nlmLogDateAndTime.setDescription('The local date and time when the entry was logged, instantiated only by systems that have date and time capability.')
nlmLogEngineID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 4), SnmpEngineID()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogEngineID.setStatus('current')
if mibBuilder.loadTexts: nlmLogEngineID.setDescription('The identification of the SNMP engine at which the Notification originated. If the log can contain Notifications from only one engine or the Trap is in SNMPv1 format, this object is a zero-length string.')
nlmLogEngineTAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 5), TAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogEngineTAddress.setStatus('current')
if mibBuilder.loadTexts: nlmLogEngineTAddress.setDescription('The transport service address of the SNMP engine from which the Notification was received, formatted according to the corresponding value of nlmLogEngineTDomain. This is used to identify the source of an SNMPv1 trap, since an nlmLogEngineId cannot be extracted from the SNMPv1 trap pdu. This object MUST always be instantiated, even if the log can contain Notifications from only one engine. Please be aware that the nlmLogEngineTAddress may not uniquely identify the SNMP engine from which the Notification was received. For example, if an SNMP engine uses DHCP or NAT to obtain ip addresses, the address it uses may be shared with other network devices, and hence will not uniquely identify the SNMP engine.')
nlmLogEngineTDomain = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 6), TDomain()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogEngineTDomain.setStatus('current')
if mibBuilder.loadTexts: nlmLogEngineTDomain.setDescription('Indicates the kind of transport service by which a Notification was received from an SNMP engine. nlmLogEngineTAddress contains the transport service address of the SNMP engine from which this Notification was received. Possible values for this object are presently found in the Transport Mappings for SNMPv2 document (RFC 1906 [8]).')
nlmLogContextEngineID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 7), SnmpEngineID()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogContextEngineID.setStatus('current')
if mibBuilder.loadTexts: nlmLogContextEngineID.setDescription('If the Notification was received in a protocol which has a contextEngineID element like SNMPv3, this object has that value. Otherwise its value is a zero-length string.')
nlmLogContextName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 8), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogContextName.setStatus('current')
if mibBuilder.loadTexts: nlmLogContextName.setDescription('The name of the SNMP MIB context from which the Notification came. For SNMPv1 Traps this is the community string from the Trap.')
nlmLogNotificationID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 9), ObjectIdentifier()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogNotificationID.setStatus('current')
if mibBuilder.loadTexts: nlmLogNotificationID.setDescription('The NOTIFICATION-TYPE object identifier of the Notification that occurred.')
nlmLogVariableTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 3, 2), )
if mibBuilder.loadTexts: nlmLogVariableTable.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableTable.setDescription('A table of variables to go with Notification log entries.')
nlmLogVariableEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1), ).setIndexNames((0, "NOTIFICATION-LOG-MIB", "nlmLogName"), (0, "NOTIFICATION-LOG-MIB", "nlmLogIndex"), (0, "NOTIFICATION-LOG-MIB", "nlmLogVariableIndex"))
if mibBuilder.loadTexts: nlmLogVariableEntry.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableEntry.setDescription('A Notification log entry variable. Entries appear in this table when there are variables in the varbind list of a Notification in nlmLogTable.')
nlmLogVariableIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts: nlmLogVariableIndex.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableIndex.setDescription('A monotonically increasing integer, starting at 1 for a given nlmLogIndex, for indexing variables within the logged Notification.')
nlmLogVariableID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 2), ObjectIdentifier()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableID.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableID.setDescription("The variable's object identifier.")
nlmLogVariableValueType = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9))).clone(namedValues=NamedValues(("counter32", 1), ("unsigned32", 2), ("timeTicks", 3), ("integer32", 4), ("ipAddress", 5), ("octetString", 6), ("objectId", 7), ("counter64", 8), ("opaque", 9)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableValueType.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableValueType.setDescription('The type of the value. One and only one of the value objects that follow must be instantiated, based on this type.')
nlmLogVariableCounter32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableCounter32Val.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableCounter32Val.setDescription("The value when nlmLogVariableType is 'counter32'.")
nlmLogVariableUnsigned32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 5), Unsigned32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableUnsigned32Val.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableUnsigned32Val.setDescription("The value when nlmLogVariableType is 'unsigned32'.")
nlmLogVariableTimeTicksVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 6), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableTimeTicksVal.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableTimeTicksVal.setDescription("The value when nlmLogVariableType is 'timeTicks'.")
nlmLogVariableInteger32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 7), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableInteger32Val.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableInteger32Val.setDescription("The value when nlmLogVariableType is 'integer32'.")
nlmLogVariableOctetStringVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 8), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableOctetStringVal.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableOctetStringVal.setDescription("The value when nlmLogVariableType is 'octetString'.")
nlmLogVariableIpAddressVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 9), IpAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableIpAddressVal.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableIpAddressVal.setDescription("The value when nlmLogVariableType is 'ipAddress'. Although this seems to be unfriendly for IPv6, we have to recognize that there are a number of older MIBs that do contain an IPv4 format address, known as IpAddress. IPv6 addresses are represented using TAddress or InetAddress, and so the underlying datatype is OCTET STRING, and their value would be stored in the nlmLogVariableOctetStringVal column.")
nlmLogVariableOidVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 10), ObjectIdentifier()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableOidVal.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableOidVal.setDescription("The value when nlmLogVariableType is 'objectId'.")
nlmLogVariableCounter64Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 11), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableCounter64Val.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableCounter64Val.setDescription("The value when nlmLogVariableType is 'counter64'.")
nlmLogVariableOpaqueVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 12), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: nlmLogVariableOpaqueVal.setStatus('current')
if mibBuilder.loadTexts: nlmLogVariableOpaqueVal.setDescription("The value when nlmLogVariableType is 'opaque'.")
notificationLogMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3))
notificationLogMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3, 1))
notificationLogMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3, 2))
notificationLogMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 92, 3, 1, 1)).setObjects(("NOTIFICATION-LOG-MIB", "notificationLogConfigGroup"), ("NOTIFICATION-LOG-MIB", "notificationLogStatsGroup"), ("NOTIFICATION-LOG-MIB", "notificationLogLogGroup"))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    notificationLogMIBCompliance = notificationLogMIBCompliance.setStatus('current')
if mibBuilder.loadTexts: notificationLogMIBCompliance.setDescription('The compliance statement for entities which implement the Notification Log MIB.')
notificationLogConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 1)).setObjects(("NOTIFICATION-LOG-MIB", "nlmConfigGlobalEntryLimit"), ("NOTIFICATION-LOG-MIB", "nlmConfigGlobalAgeOut"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogFilterName"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogEntryLimit"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogAdminStatus"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogOperStatus"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogStorageType"), ("NOTIFICATION-LOG-MIB", "nlmConfigLogEntryStatus"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    notificationLogConfigGroup = notificationLogConfigGroup.setStatus('current')
if mibBuilder.loadTexts: notificationLogConfigGroup.setDescription('Notification log configuration management.')
notificationLogStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 2)).setObjects(("NOTIFICATION-LOG-MIB", "nlmStatsGlobalNotificationsLogged"), ("NOTIFICATION-LOG-MIB", "nlmStatsGlobalNotificationsBumped"), ("NOTIFICATION-LOG-MIB", "nlmStatsLogNotificationsLogged"), ("NOTIFICATION-LOG-MIB", "nlmStatsLogNotificationsBumped"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    notificationLogStatsGroup = notificationLogStatsGroup.setStatus('current')
if mibBuilder.loadTexts: notificationLogStatsGroup.setDescription('Notification log statistics.')
notificationLogLogGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 3)).setObjects(("NOTIFICATION-LOG-MIB", "nlmLogTime"), ("NOTIFICATION-LOG-MIB", "nlmLogEngineID"), ("NOTIFICATION-LOG-MIB", "nlmLogEngineTAddress"), ("NOTIFICATION-LOG-MIB", "nlmLogEngineTDomain"), ("NOTIFICATION-LOG-MIB", "nlmLogContextEngineID"), ("NOTIFICATION-LOG-MIB", "nlmLogContextName"), ("NOTIFICATION-LOG-MIB", "nlmLogNotificationID"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableID"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableValueType"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableCounter32Val"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableUnsigned32Val"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableTimeTicksVal"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableInteger32Val"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableOctetStringVal"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableIpAddressVal"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableOidVal"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableCounter64Val"), ("NOTIFICATION-LOG-MIB", "nlmLogVariableOpaqueVal"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    notificationLogLogGroup = notificationLogLogGroup.setStatus('current')
if mibBuilder.loadTexts: notificationLogLogGroup.setDescription('Notification log data.')
notificationLogDateGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 4)).setObjects(("NOTIFICATION-LOG-MIB", "nlmLogDateAndTime"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    notificationLogDateGroup = notificationLogDateGroup.setStatus('current')
if mibBuilder.loadTexts: notificationLogDateGroup.setDescription('Conditionally mandatory notification log data. This group is mandatory on systems that keep wall clock date and time and should not be implemented on systems that do not have a wall clock date.')
mibBuilder.exportSymbols("NOTIFICATION-LOG-MIB", nlmConfigGlobalEntryLimit=nlmConfigGlobalEntryLimit, nlmLogEntry=nlmLogEntry, nlmStatsLogTable=nlmStatsLogTable, notificationLogMIBCompliance=notificationLogMIBCompliance, nlmLogIndex=nlmLogIndex, nlmConfigLogEntryLimit=nlmConfigLogEntryLimit, nlmLogTime=nlmLogTime, notificationLogDateGroup=notificationLogDateGroup, nlmStatsLogNotificationsLogged=nlmStatsLogNotificationsLogged, nlmConfigLogFilterName=nlmConfigLogFilterName, nlmStatsLogEntry=nlmStatsLogEntry, nlmLogEngineTAddress=nlmLogEngineTAddress, nlmLogVariableIndex=nlmLogVariableIndex, nlmLogEngineTDomain=nlmLogEngineTDomain, nlmLogVariableCounter64Val=nlmLogVariableCounter64Val, nlmStatsLogNotificationsBumped=nlmStatsLogNotificationsBumped, nlmLogDateAndTime=nlmLogDateAndTime, nlmLogTable=nlmLogTable, notificationLogStatsGroup=notificationLogStatsGroup, nlmLog=nlmLog, notificationLogMIBObjects=notificationLogMIBObjects, nlmLogName=nlmLogName, nlmConfigLogOperStatus=nlmConfigLogOperStatus, nlmConfigLogEntryStatus=nlmConfigLogEntryStatus, nlmLogContextName=nlmLogContextName, nlmLogVariableOctetStringVal=nlmLogVariableOctetStringVal, nlmLogVariableIpAddressVal=nlmLogVariableIpAddressVal, nlmLogVariableOidVal=nlmLogVariableOidVal, nlmLogVariableEntry=nlmLogVariableEntry, nlmConfigLogTable=nlmConfigLogTable, notificationLogMIBGroups=notificationLogMIBGroups, nlmConfigLogStorageType=nlmConfigLogStorageType, nlmLogVariableCounter32Val=nlmLogVariableCounter32Val, notificationLogMIBCompliances=notificationLogMIBCompliances, nlmConfig=nlmConfig, notificationLogMIBConformance=notificationLogMIBConformance, notificationLogMIB=notificationLogMIB, nlmStats=nlmStats, PYSNMP_MODULE_ID=notificationLogMIB, nlmLogVariableID=nlmLogVariableID, nlmStatsGlobalNotificationsLogged=nlmStatsGlobalNotificationsLogged, notificationLogConfigGroup=notificationLogConfigGroup, nlmLogVariableTimeTicksVal=nlmLogVariableTimeTicksVal, nlmConfigGlobalAgeOut=nlmConfigGlobalAgeOut, nlmStatsGlobalNotificationsBumped=nlmStatsGlobalNotificationsBumped, nlmLogVariableInteger32Val=nlmLogVariableInteger32Val, nlmLogVariableUnsigned32Val=nlmLogVariableUnsigned32Val, nlmLogEngineID=nlmLogEngineID, nlmLogVariableTable=nlmLogVariableTable, notificationLogLogGroup=notificationLogLogGroup, nlmConfigLogEntry=nlmConfigLogEntry, nlmLogNotificationID=nlmLogNotificationID, nlmLogVariableValueType=nlmLogVariableValueType, nlmConfigLogAdminStatus=nlmConfigLogAdminStatus, nlmLogVariableOpaqueVal=nlmLogVariableOpaqueVal, nlmLogContextEngineID=nlmLogContextEngineID)