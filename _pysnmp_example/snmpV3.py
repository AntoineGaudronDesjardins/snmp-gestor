from pysnmp.hlapi import *

## Available authentication protocols:

#     usmHMACMD5AuthProtocol
#     usmHMACSHAAuthProtocol
#     usmHMAC128SHA224AuthProtocol
#     usmHMAC192SHA256AuthProtocol
#     usmHMAC256SHA384AuthProtocol
#     usmHMAC384SHA512AuthProtocol
#     usmNoAuthProtocol

## Available privacy protocols:

#     usmDESPrivProtocol
#     usm3DESEDEPrivProtocol
#     usmAesCfb128Protocol
#     usmAesCfb192Protocol
#     usmAesCfb256Protocol
#     usmNoPrivProtocol


iterator = setCmd(
    SnmpEngine(),
    UsmUserData('antoine', 'password', 'password',
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmAesCfb128Protocol),
    UdpTransportTarget(('192.168.31.10', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), 'location')
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))