#
# PySNMP MIB module PYSNMP-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://C:\Users\antoi\OneDrive - CentraleSupelec\ETSI\gestion_de_redes\proyecto\pythonScripts\mibs\mibs\PYSNMP-MIB.mib
# Produced by pysmi-0.3.4 at Mon Apr 24 01:14:58 2023
# On host ? platform ? version ? by user ?
# Using Python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]
#
ObjectIdentifier, OctetString, Integer = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint")
NotificationGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
iso, enterprises, TimeTicks, IpAddress, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, ObjectIdentity, NotificationType, Integer32, Counter64, Gauge32, Counter32, Unsigned32, MibIdentifier, Bits = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "enterprises", "TimeTicks", "IpAddress", "ModuleIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "ObjectIdentity", "NotificationType", "Integer32", "Counter64", "Gauge32", "Counter32", "Unsigned32", "MibIdentifier", "Bits")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
pysnmp = ModuleIdentity((1, 3, 6, 1, 4, 1, 20408))
pysnmp.setRevisions(('2017-04-14 00:00', '2005-05-14 00:00',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: pysnmp.setRevisionsDescriptions(('Updated addresses', 'Initial revision',))
if mibBuilder.loadTexts: pysnmp.setLastUpdated('201704140000Z')
if mibBuilder.loadTexts: pysnmp.setOrganization('The PySNMP Project')
if mibBuilder.loadTexts: pysnmp.setContactInfo('E-mail: Ilya Etingof <etingof@gmail.com> GitHub: https://github.com/etingof/pysnmp')
if mibBuilder.loadTexts: pysnmp.setDescription('PySNMP top-level MIB tree infrastructure')
pysnmpObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 1))
pysnmpExamples = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 2))
pysnmpEnumerations = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3))
pysnmpModuleIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1))
pysnmpAgentOIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 2))
pysnmpDomains = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 3))
pysnmpExperimental = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 9999))
pysnmpNotificationPrefix = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4))
pysnmpNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4, 0))
pysnmpNotificationObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4, 1))
pysnmpConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5))
pysnmpCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5, 1))
pysnmpGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5, 2))
mibBuilder.exportSymbols("PYSNMP-MIB", pysnmpConformance=pysnmpConformance, pysnmpEnumerations=pysnmpEnumerations, pysnmpNotificationPrefix=pysnmpNotificationPrefix, pysnmpDomains=pysnmpDomains, pysnmpCompliances=pysnmpCompliances, pysnmpModuleIDs=pysnmpModuleIDs, pysnmpAgentOIDs=pysnmpAgentOIDs, pysnmpExperimental=pysnmpExperimental, pysnmpNotifications=pysnmpNotifications, pysnmpObjects=pysnmpObjects, pysnmpNotificationObjects=pysnmpNotificationObjects, pysnmp=pysnmp, pysnmpGroups=pysnmpGroups, PYSNMP_MODULE_ID=pysnmp, pysnmpExamples=pysnmpExamples)
