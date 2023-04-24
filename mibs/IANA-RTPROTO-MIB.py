#
# PySNMP MIB module IANA-RTPROTO-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://C:\Users\antoi\OneDrive - CentraleSupelec\ETSI\gestion_de_redes\proyecto\pythonScripts\mibs\mibs\IANA-RTPROTO-MIB.mib
# Produced by pysmi-0.3.4 at Mon Apr 24 01:14:58 2023
# On host ? platform ? version ? by user ?
# Using Python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]
#
ObjectIdentifier, OctetString, Integer = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint")
NotificationGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
iso, TimeTicks, IpAddress, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, ObjectIdentity, NotificationType, Integer32, Counter64, Gauge32, Counter32, Unsigned32, MibIdentifier, mib_2, Bits = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "TimeTicks", "IpAddress", "ModuleIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "ObjectIdentity", "NotificationType", "Integer32", "Counter64", "Gauge32", "Counter32", "Unsigned32", "MibIdentifier", "mib-2", "Bits")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
ianaRtProtoMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 84))
ianaRtProtoMIB.setRevisions(('2000-09-26 00:00',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: ianaRtProtoMIB.setRevisionsDescriptions(('Original version, published in coordination with RFC 2932.',))
if mibBuilder.loadTexts: ianaRtProtoMIB.setLastUpdated('200009260000Z')
if mibBuilder.loadTexts: ianaRtProtoMIB.setOrganization('IANA')
if mibBuilder.loadTexts: ianaRtProtoMIB.setContactInfo(' Internet Assigned Numbers Authority Internet Corporation for Assigned Names and Numbers 4676 Admiralty Way, Suite 330 Marina del Rey, CA 90292-6601 Phone: +1 310 823 9358 EMail: iana@iana.org')
if mibBuilder.loadTexts: ianaRtProtoMIB.setDescription('This MIB module defines the IANAipRouteProtocol and IANAipMRouteProtocol textual conventions for use in MIBs which need to identify unicast or multicast routing mechanisms. Any additions or changes to the contents of this MIB module require either publication of an RFC, or Designated Expert Review as defined in RFC 2434, Guidelines for Writing an IANA Considerations Section in RFCs. The Designated Expert will be selected by the IESG Area Director(s) of the Routing Area.')
class IANAipRouteProtocol(TextualConvention, Integer32):
    description = 'A mechanism for learning routes. Inclusion of values for routing protocols is not intended to imply that those protocols need be supported.'
    status = 'current'
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17))
    namedValues = NamedValues(("other", 1), ("local", 2), ("netmgmt", 3), ("icmp", 4), ("egp", 5), ("ggp", 6), ("hello", 7), ("rip", 8), ("isIs", 9), ("esIs", 10), ("ciscoIgrp", 11), ("bbnSpfIgp", 12), ("ospf", 13), ("bgp", 14), ("idpr", 15), ("ciscoEigrp", 16), ("dvmrp", 17))

class IANAipMRouteProtocol(TextualConvention, Integer32):
    description = 'The multicast routing protocol. Inclusion of values for multicast routing protocols is not intended to imply that those protocols need be supported.'
    status = 'current'
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    namedValues = NamedValues(("other", 1), ("local", 2), ("netmgmt", 3), ("dvmrp", 4), ("mospf", 5), ("pimSparseDense", 6), ("cbt", 7), ("pimSparseMode", 8), ("pimDenseMode", 9), ("igmpOnly", 10), ("bgmp", 11), ("msdp", 12))

mibBuilder.exportSymbols("IANA-RTPROTO-MIB", PYSNMP_MODULE_ID=ianaRtProtoMIB, IANAipRouteProtocol=IANAipRouteProtocol, ianaRtProtoMIB=ianaRtProtoMIB, IANAipMRouteProtocol=IANAipMRouteProtocol)
