from pysnmp.hlapi import *

iterator = nextCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget(('192.168.31.12', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0))
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