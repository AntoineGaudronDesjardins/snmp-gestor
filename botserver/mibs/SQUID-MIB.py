#
# PySNMP MIB module SQUID-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://C:\Users\antoi\OneDrive - CentraleSupelec\ETSI\gestion_de_redes\proyecto\snmp-gestor\mibs\mibs\SQUID-MIB.mib
# Produced by pysmi-0.3.4 at Thu May  4 19:59:26 2023
# On host ? platform ? version ? by user ?
# Using Python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]
#
Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ConstraintsIntersection")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
iso, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter32, MibIdentifier, TimeTicks, Integer32, enterprises, Bits, NotificationType, ModuleIdentity, Unsigned32, ObjectIdentity, Gauge32, Counter64 = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "IpAddress", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter32", "MibIdentifier", "TimeTicks", "Integer32", "enterprises", "Bits", "NotificationType", "ModuleIdentity", "Unsigned32", "ObjectIdentity", "Gauge32", "Counter64")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
nlanr = MibIdentifier((1, 3, 6, 1, 4, 1, 3495))
squid = ModuleIdentity((1, 3, 6, 1, 4, 1, 3495, 1))
squid.setRevisions(('1998-09-22 00:00', '1999-01-01 00:00',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: squid.setRevisionsDescriptions(('Move to SMIv2. Prepare to split into proxy/squid.', 'Added objects and corrected asn.1 syntax and descriptions.',))
if mibBuilder.loadTexts: squid.setLastUpdated('9809220000Z')
if mibBuilder.loadTexts: squid.setOrganization('National Laboratory for Applied Network Research')
if mibBuilder.loadTexts: squid.setContactInfo(' Squid Developers E-mail: squid@squid-cache.org')
if mibBuilder.loadTexts: squid.setDescription('Squid MIB defined for the management of the Squid proxy server. See http://www.squid-cache.org/.')
cacheSystem = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 1))
cacheConfig = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 2))
cachePerf = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 3))
cacheNetwork = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 4))
cacheMesh = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 5))
cacheSysVMsize = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSysVMsize.setStatus('current')
if mibBuilder.loadTexts: cacheSysVMsize.setDescription(' Storage Mem size in KB ')
cacheSysStorage = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 1, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSysStorage.setStatus('current')
if mibBuilder.loadTexts: cacheSysStorage.setDescription(' Storage Swap size in KB ')
cacheUptime = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 1, 3), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheUptime.setStatus('current')
if mibBuilder.loadTexts: cacheUptime.setDescription(' The Uptime of the cache in timeticks ')
cacheAdmin = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 1), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheAdmin.setStatus('current')
if mibBuilder.loadTexts: cacheAdmin.setDescription(' Cache Administrator E-Mail address ')
cacheSoftware = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 2), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSoftware.setStatus('current')
if mibBuilder.loadTexts: cacheSoftware.setDescription(' Cache Software Name ')
cacheVersionId = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 3), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheVersionId.setStatus('current')
if mibBuilder.loadTexts: cacheVersionId.setDescription(' Cache Software Version ')
cacheLoggingFacility = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 4), DisplayString()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: cacheLoggingFacility.setStatus('current')
if mibBuilder.loadTexts: cacheLoggingFacility.setDescription(' Logging Facility. An informational string indicating logging info like debug level, local/syslog/remote logging etc ')
cacheStorageConfig = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 2, 5))
cacheMemMaxSize = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 5, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheMemMaxSize.setStatus('current')
if mibBuilder.loadTexts: cacheMemMaxSize.setDescription(' The value of the cache_mem parameter in MB ')
cacheSwapMaxSize = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 5, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSwapMaxSize.setStatus('current')
if mibBuilder.loadTexts: cacheSwapMaxSize.setDescription(' The total of the cache_dir space allocated in MB ')
cacheSwapHighWM = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 5, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSwapHighWM.setStatus('current')
if mibBuilder.loadTexts: cacheSwapHighWM.setDescription(' Cache Swap High Water Mark ')
cacheSwapLowWM = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 2, 5, 4), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSwapLowWM.setStatus('current')
if mibBuilder.loadTexts: cacheSwapLowWM.setDescription(' Cache Swap Low Water Mark ')
cacheSysPerf = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1))
cacheProtoStats = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2))
cacheSysPageFaults = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheSysPageFaults.setStatus('current')
if mibBuilder.loadTexts: cacheSysPageFaults.setDescription(' Page faults with physical i/o ')
cacheSysNumReads = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 2), Counter32())
if mibBuilder.loadTexts: cacheSysNumReads.setStatus('current')
if mibBuilder.loadTexts: cacheSysNumReads.setDescription(' HTTP I/O number of reads ')
cacheMemUsage = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheMemUsage.setStatus('current')
if mibBuilder.loadTexts: cacheMemUsage.setDescription(' Total memory accounted for KB ')
cacheCpuTime = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 4), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCpuTime.setStatus('current')
if mibBuilder.loadTexts: cacheCpuTime.setDescription(' Amount of cpu seconds consumed ')
cacheCpuUsage = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 5), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCpuUsage.setStatus('current')
if mibBuilder.loadTexts: cacheCpuUsage.setDescription(' The percentage use of the CPU ')
cacheMaxResSize = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 6), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheMaxResSize.setStatus('current')
if mibBuilder.loadTexts: cacheMaxResSize.setDescription(' Maximum Resident Size in KB ')
cacheNumObjCount = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheNumObjCount.setStatus('current')
if mibBuilder.loadTexts: cacheNumObjCount.setDescription(' Number of objects stored by the cache ')
cacheCurrentLRUExpiration = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 8), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCurrentLRUExpiration.setStatus('current')
if mibBuilder.loadTexts: cacheCurrentLRUExpiration.setDescription(' Storage LRU Expiration Age ')
cacheCurrentUnlinkRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCurrentUnlinkRequests.setStatus('current')
if mibBuilder.loadTexts: cacheCurrentUnlinkRequests.setDescription(' Requests given to unlinkd ')
cacheCurrentUnusedFDescrCnt = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 10), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCurrentUnusedFDescrCnt.setStatus('current')
if mibBuilder.loadTexts: cacheCurrentUnusedFDescrCnt.setDescription(' Available number of file descriptors ')
cacheCurrentResFileDescrCnt = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 1, 11), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCurrentResFileDescrCnt.setStatus('current')
if mibBuilder.loadTexts: cacheCurrentResFileDescrCnt.setDescription(' Reserved number of file descriptors ')
cacheProtoAggregateStats = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1))
cacheProtoClientHttpRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheProtoClientHttpRequests.setStatus('current')
if mibBuilder.loadTexts: cacheProtoClientHttpRequests.setDescription(' Number of HTTP requests received ')
cacheHttpHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpHits.setStatus('current')
if mibBuilder.loadTexts: cacheHttpHits.setDescription(' Number of HTTP Hits ')
cacheHttpErrors = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpErrors.setStatus('current')
if mibBuilder.loadTexts: cacheHttpErrors.setDescription(' Number of HTTP Errors ')
cacheHttpInKb = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpInKb.setStatus('current')
if mibBuilder.loadTexts: cacheHttpInKb.setDescription(" Number of HTTP KB's recieved ")
cacheHttpOutKb = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpOutKb.setStatus('current')
if mibBuilder.loadTexts: cacheHttpOutKb.setDescription(" Number of HTTP KB's transmitted ")
cacheIcpPktsSent = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpPktsSent.setStatus('current')
if mibBuilder.loadTexts: cacheIcpPktsSent.setDescription(' Number of ICP messages sent ')
cacheIcpPktsRecv = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpPktsRecv.setStatus('current')
if mibBuilder.loadTexts: cacheIcpPktsRecv.setDescription(' Number of ICP messages received ')
cacheIcpKbSent = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpKbSent.setStatus('current')
if mibBuilder.loadTexts: cacheIcpKbSent.setDescription(" Number of ICP KB's transmitted ")
cacheIcpKbRecv = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpKbRecv.setStatus('current')
if mibBuilder.loadTexts: cacheIcpKbRecv.setDescription(" Number of ICP KB's recieved ")
cacheServerRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 10), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheServerRequests.setStatus('current')
if mibBuilder.loadTexts: cacheServerRequests.setDescription(' All requests from the client for the cache server ')
cacheServerErrors = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 11), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheServerErrors.setStatus('current')
if mibBuilder.loadTexts: cacheServerErrors.setDescription(' All errors for the cache server from client requests ')
cacheServerInKb = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 12), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheServerInKb.setStatus('current')
if mibBuilder.loadTexts: cacheServerInKb.setDescription(" KB's of traffic recieved from servers ")
cacheServerOutKb = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 13), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheServerOutKb.setStatus('current')
if mibBuilder.loadTexts: cacheServerOutKb.setDescription(" KB's of traffic sent to servers ")
cacheCurrentSwapSize = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 14), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheCurrentSwapSize.setStatus('current')
if mibBuilder.loadTexts: cacheCurrentSwapSize.setDescription(' Storage Swap size ')
cacheClients = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 1, 15), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClients.setStatus('current')
if mibBuilder.loadTexts: cacheClients.setDescription(' Number of clients accessing cache ')
cacheMedianSvcTable = MibTable((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2), ).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheMedianSvcTable.setStatus('current')
if mibBuilder.loadTexts: cacheMedianSvcTable.setDescription(' CacheMedianSvcTable ')
cacheMedianSvcEntry = MibTableRow((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1), ).setIndexNames((0, "SQUID-MIB", "cacheMedianTime"))
if mibBuilder.loadTexts: cacheMedianSvcEntry.setStatus('current')
if mibBuilder.loadTexts: cacheMedianSvcEntry.setDescription(' An entry in cacheMedianSvcTable ')
cacheMedianTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheMedianTime.setStatus('current')
if mibBuilder.loadTexts: cacheMedianTime.setDescription(' The value used to index the table 1/5/60')
cacheHttpAllSvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpAllSvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheHttpAllSvcTime.setDescription(' HTTP all service time ')
cacheHttpMissSvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpMissSvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheHttpMissSvcTime.setDescription(' HTTP miss service time ')
cacheHttpNmSvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 4), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpNmSvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheHttpNmSvcTime.setDescription(' HTTP near miss service time ')
cacheHttpHitSvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 5), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheHttpHitSvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheHttpHitSvcTime.setDescription(' HTTP hit service time ')
cacheIcpQuerySvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 6), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpQuerySvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheIcpQuerySvcTime.setDescription(' ICP query service time ')
cacheIcpReplySvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 7), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIcpReplySvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheIcpReplySvcTime.setDescription(' ICP reply service time ')
cacheDnsSvcTime = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 8), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheDnsSvcTime.setStatus('current')
if mibBuilder.loadTexts: cacheDnsSvcTime.setDescription(' DNS service time ')
cacheRequestHitRatio = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 9), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheRequestHitRatio.setStatus('current')
if mibBuilder.loadTexts: cacheRequestHitRatio.setDescription(' Request Hit Ratios ')
cacheRequestByteRatio = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 3, 2, 2, 1, 10), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheRequestByteRatio.setStatus('current')
if mibBuilder.loadTexts: cacheRequestByteRatio.setDescription(' Byte Hit Ratios ')
cacheIpCache = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1))
cacheFqdnCache = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2))
cacheDns = MibIdentifier((1, 3, 6, 1, 4, 1, 3495, 1, 4, 3))
cacheIpEntries = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 1), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpEntries.setStatus('current')
if mibBuilder.loadTexts: cacheIpEntries.setDescription(' IP Cache Entries ')
cacheIpRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpRequests.setStatus('current')
if mibBuilder.loadTexts: cacheIpRequests.setDescription(' Number of IP Cache requests ')
cacheIpHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpHits.setStatus('current')
if mibBuilder.loadTexts: cacheIpHits.setDescription(' Number of IP Cache hits ')
cacheIpPendingHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 4), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpPendingHits.setStatus('current')
if mibBuilder.loadTexts: cacheIpPendingHits.setDescription(' Number of IP Cache pending hits ')
cacheIpNegativeHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpNegativeHits.setStatus('current')
if mibBuilder.loadTexts: cacheIpNegativeHits.setDescription(' Number of IP Cache negative hits ')
cacheIpMisses = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheIpMisses.setStatus('current')
if mibBuilder.loadTexts: cacheIpMisses.setDescription(' Number of IP Cache misses ')
cacheBlockingGetHostByName = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheBlockingGetHostByName.setStatus('current')
if mibBuilder.loadTexts: cacheBlockingGetHostByName.setDescription(' Number of blocking gethostbyname requests ')
cacheAttemptReleaseLckEntries = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheAttemptReleaseLckEntries.setStatus('current')
if mibBuilder.loadTexts: cacheAttemptReleaseLckEntries.setDescription(' Number of attempts to release locked IP Cache entries ')
cacheFqdnEntries = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 1), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnEntries.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnEntries.setDescription(' FQDN Cache entries ')
cacheFqdnRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnRequests.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnRequests.setDescription(' Number of FQDN Cache requests ')
cacheFqdnHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnHits.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnHits.setDescription(' Number of FQDN Cache hits ')
cacheFqdnPendingHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 4), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnPendingHits.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnPendingHits.setDescription(' Number of FQDN Cache pending hits ')
cacheFqdnNegativeHits = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnNegativeHits.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnNegativeHits.setDescription(' Number of FQDN Cache negative hits ')
cacheFqdnMisses = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheFqdnMisses.setStatus('current')
if mibBuilder.loadTexts: cacheFqdnMisses.setDescription(' Number of FQDN Cache misses ')
cacheBlockingGetHostByAddr = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 2, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheBlockingGetHostByAddr.setStatus('current')
if mibBuilder.loadTexts: cacheBlockingGetHostByAddr.setDescription(' Number of blocking gethostbyaddr requests ')
cacheDnsRequests = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 3, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheDnsRequests.setStatus('current')
if mibBuilder.loadTexts: cacheDnsRequests.setDescription(' Number of external dnsserver requests ')
cacheDnsReplies = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 3, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheDnsReplies.setStatus('current')
if mibBuilder.loadTexts: cacheDnsReplies.setDescription(' Number of external dnsserver replies ')
cacheDnsNumberServers = MibScalar((1, 3, 6, 1, 4, 1, 3495, 1, 4, 3, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheDnsNumberServers.setStatus('current')
if mibBuilder.loadTexts: cacheDnsNumberServers.setDescription(' Number of external dnsserver processes ')
cachePeerTable = MibTable((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1), ).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerTable.setStatus('current')
if mibBuilder.loadTexts: cachePeerTable.setDescription(' This table contains an enumeration of the peer caches, complete with info ')
cachePeerEntry = MibTableRow((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1), ).setIndexNames((0, "SQUID-MIB", "cachePeerAddr"))
if mibBuilder.loadTexts: cachePeerEntry.setStatus('current')
if mibBuilder.loadTexts: cachePeerEntry.setDescription(' An entry in cachePeerTable ')
cachePeerName = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 1), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerName.setStatus('current')
if mibBuilder.loadTexts: cachePeerName.setDescription(' The FQDN name or internal alias for the peer cache ')
cachePeerAddr = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 2), IpAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerAddr.setStatus('current')
if mibBuilder.loadTexts: cachePeerAddr.setDescription(' The IP Address of the peer cache ')
cachePeerPortHttp = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerPortHttp.setStatus('current')
if mibBuilder.loadTexts: cachePeerPortHttp.setDescription(' The port the peer listens for HTTP requests ')
cachePeerPortIcp = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 4), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerPortIcp.setStatus('current')
if mibBuilder.loadTexts: cachePeerPortIcp.setDescription(' The port the peer listens for ICP requests should be 0 if not configured to send ICP requests ')
cachePeerType = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 5), Integer32())
if mibBuilder.loadTexts: cachePeerType.setStatus('current')
if mibBuilder.loadTexts: cachePeerType.setDescription(' Peer Type ')
cachePeerState = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 6), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerState.setStatus('current')
if mibBuilder.loadTexts: cachePeerState.setDescription(' The operational state of this peer ')
cachePeerPingsSent = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerPingsSent.setStatus('current')
if mibBuilder.loadTexts: cachePeerPingsSent.setDescription(' Number of pings sent to peer ')
cachePeerPingsAcked = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerPingsAcked.setStatus('current')
if mibBuilder.loadTexts: cachePeerPingsAcked.setDescription(' Number of pings received from peer ')
cachePeerFetches = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerFetches.setStatus('current')
if mibBuilder.loadTexts: cachePeerFetches.setDescription(' Number of times this peer was selected ')
cachePeerRtt = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 10), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerRtt.setStatus('current')
if mibBuilder.loadTexts: cachePeerRtt.setDescription(' Last known round-trip time to the peer (in ms) ')
cachePeerIgnored = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 11), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerIgnored.setStatus('current')
if mibBuilder.loadTexts: cachePeerIgnored.setDescription(' How many times this peer was ignored ')
cachePeerKeepAlSent = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 12), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerKeepAlSent.setStatus('current')
if mibBuilder.loadTexts: cachePeerKeepAlSent.setDescription(' Number of keepalives sent ')
cachePeerKeepAlRecv = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 1, 1, 13), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cachePeerKeepAlRecv.setStatus('current')
if mibBuilder.loadTexts: cachePeerKeepAlRecv.setDescription(' Number of keepalives received ')
cacheClientTable = MibTable((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2), )
if mibBuilder.loadTexts: cacheClientTable.setStatus('mandatory')
if mibBuilder.loadTexts: cacheClientTable.setDescription('A list of cache client entries.')
cacheClientEntry = MibTableRow((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1), ).setIndexNames((0, "SQUID-MIB", "cacheClientAddr"))
if mibBuilder.loadTexts: cacheClientEntry.setStatus('mandatory')
if mibBuilder.loadTexts: cacheClientEntry.setDescription('An entry in cacheClientTable ')
cacheClientAddr = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 1), IpAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientAddr.setStatus('current')
if mibBuilder.loadTexts: cacheClientAddr.setDescription("The client's IP address ")
cacheClientHttpRequests = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientHttpRequests.setStatus('current')
if mibBuilder.loadTexts: cacheClientHttpRequests.setDescription(' Number of HTTP requests received from client ')
cacheClientHttpKb = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientHttpKb.setStatus('current')
if mibBuilder.loadTexts: cacheClientHttpKb.setDescription(' Amount of total HTTP traffic to this client ')
cacheClientHttpHits = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientHttpHits.setStatus('current')
if mibBuilder.loadTexts: cacheClientHttpHits.setDescription(" Number of hits in response to this client's HTTP requests ")
cacheClientHTTPHitKb = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientHTTPHitKb.setStatus('current')
if mibBuilder.loadTexts: cacheClientHTTPHitKb.setDescription(' Amount of HTTP hit traffic in KB ')
cacheClientIcpRequests = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientIcpRequests.setStatus('current')
if mibBuilder.loadTexts: cacheClientIcpRequests.setDescription(' Number of ICP requests received from client ')
cacheClientIcpKb = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientIcpKb.setStatus('current')
if mibBuilder.loadTexts: cacheClientIcpKb.setDescription(' Amount of total ICP traffic to this client (child) ')
cacheClientIcpHits = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientIcpHits.setStatus('current')
if mibBuilder.loadTexts: cacheClientIcpHits.setDescription(" Number of hits in response to this client's ICP requests ")
cacheClientIcpHitKb = MibTableColumn((1, 3, 6, 1, 4, 1, 3495, 1, 5, 2, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: cacheClientIcpHitKb.setStatus('current')
if mibBuilder.loadTexts: cacheClientIcpHitKb.setDescription(' Amount of ICP hit traffic in KB ')
mibBuilder.exportSymbols("SQUID-MIB", cachePeerKeepAlSent=cachePeerKeepAlSent, cacheSystem=cacheSystem, cachePeerAddr=cachePeerAddr, cacheDnsReplies=cacheDnsReplies, nlanr=nlanr, cacheSwapMaxSize=cacheSwapMaxSize, cacheServerInKb=cacheServerInKb, cacheClientHTTPHitKb=cacheClientHTTPHitKb, cacheCurrentSwapSize=cacheCurrentSwapSize, cacheMemUsage=cacheMemUsage, cacheCurrentResFileDescrCnt=cacheCurrentResFileDescrCnt, cacheStorageConfig=cacheStorageConfig, cacheConfig=cacheConfig, cacheFqdnRequests=cacheFqdnRequests, cacheCpuUsage=cacheCpuUsage, cacheAdmin=cacheAdmin, cacheIcpQuerySvcTime=cacheIcpQuerySvcTime, cacheDnsRequests=cacheDnsRequests, cachePeerFetches=cachePeerFetches, cacheClientEntry=cacheClientEntry, cacheClientIcpHits=cacheClientIcpHits, cacheFqdnHits=cacheFqdnHits, cacheClientHttpRequests=cacheClientHttpRequests, cacheCurrentUnlinkRequests=cacheCurrentUnlinkRequests, cacheDns=cacheDns, cacheHttpInKb=cacheHttpInKb, cacheIpEntries=cacheIpEntries, cachePeerTable=cachePeerTable, squid=squid, cacheServerRequests=cacheServerRequests, cacheClientHttpKb=cacheClientHttpKb, cachePeerPortHttp=cachePeerPortHttp, cacheHttpErrors=cacheHttpErrors, cacheFqdnPendingHits=cacheFqdnPendingHits, cacheHttpHits=cacheHttpHits, cacheMedianTime=cacheMedianTime, cacheProtoStats=cacheProtoStats, cacheIpMisses=cacheIpMisses, cachePeerState=cachePeerState, cacheMemMaxSize=cacheMemMaxSize, cacheClients=cacheClients, cacheRequestHitRatio=cacheRequestHitRatio, cacheFqdnMisses=cacheFqdnMisses, cachePeerKeepAlRecv=cachePeerKeepAlRecv, cacheSoftware=cacheSoftware, cacheClientHttpHits=cacheClientHttpHits, cacheSysNumReads=cacheSysNumReads, cacheCurrentLRUExpiration=cacheCurrentLRUExpiration, cacheIpCache=cacheIpCache, cacheSysPerf=cacheSysPerf, cacheHttpHitSvcTime=cacheHttpHitSvcTime, cacheHttpNmSvcTime=cacheHttpNmSvcTime, cacheCurrentUnusedFDescrCnt=cacheCurrentUnusedFDescrCnt, cacheClientAddr=cacheClientAddr, cacheNetwork=cacheNetwork, cacheClientIcpKb=cacheClientIcpKb, cacheSysVMsize=cacheSysVMsize, cacheNumObjCount=cacheNumObjCount, cacheDnsSvcTime=cacheDnsSvcTime, cacheIcpKbSent=cacheIcpKbSent, cacheVersionId=cacheVersionId, cacheMedianSvcEntry=cacheMedianSvcEntry, cacheSwapHighWM=cacheSwapHighWM, cachePeerPingsAcked=cachePeerPingsAcked, cacheIpHits=cacheIpHits, cacheFqdnEntries=cacheFqdnEntries, cacheFqdnCache=cacheFqdnCache, cacheMedianSvcTable=cacheMedianSvcTable, cacheBlockingGetHostByName=cacheBlockingGetHostByName, cacheIcpPktsRecv=cacheIcpPktsRecv, cacheClientIcpRequests=cacheClientIcpRequests, cacheRequestByteRatio=cacheRequestByteRatio, cacheSysStorage=cacheSysStorage, cacheBlockingGetHostByAddr=cacheBlockingGetHostByAddr, cacheIcpReplySvcTime=cacheIcpReplySvcTime, cacheFqdnNegativeHits=cacheFqdnNegativeHits, cacheIcpKbRecv=cacheIcpKbRecv, cacheAttemptReleaseLckEntries=cacheAttemptReleaseLckEntries, cacheProtoClientHttpRequests=cacheProtoClientHttpRequests, cacheServerOutKb=cacheServerOutKb, cacheIcpPktsSent=cacheIcpPktsSent, PYSNMP_MODULE_ID=squid, cachePeerName=cachePeerName, cacheHttpAllSvcTime=cacheHttpAllSvcTime, cacheMesh=cacheMesh, cachePeerEntry=cachePeerEntry, cachePeerIgnored=cachePeerIgnored, cachePeerType=cachePeerType, cachePeerRtt=cachePeerRtt, cacheClientIcpHitKb=cacheClientIcpHitKb, cacheCpuTime=cacheCpuTime, cacheHttpOutKb=cacheHttpOutKb, cacheProtoAggregateStats=cacheProtoAggregateStats, cacheSysPageFaults=cacheSysPageFaults, cacheSwapLowWM=cacheSwapLowWM, cacheDnsNumberServers=cacheDnsNumberServers, cacheHttpMissSvcTime=cacheHttpMissSvcTime, cacheIpPendingHits=cacheIpPendingHits, cacheUptime=cacheUptime, cacheServerErrors=cacheServerErrors, cacheMaxResSize=cacheMaxResSize, cachePeerPortIcp=cachePeerPortIcp, cacheIpNegativeHits=cacheIpNegativeHits, cacheClientTable=cacheClientTable, cacheIpRequests=cacheIpRequests, cacheLoggingFacility=cacheLoggingFacility, cachePeerPingsSent=cachePeerPingsSent, cachePerf=cachePerf)