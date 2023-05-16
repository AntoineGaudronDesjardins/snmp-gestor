from pysnmp.hlapi import *

iterator = bulkCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=1),
    UdpTransportTarget(('192.168.31.12', 161)),
    ContextData(),
    1,3,
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact')),
    ObjectType(ObjectIdentity((1, 3, 6, 1, 2, 1, 2, 2))),

)

for errorIndication, errorStatus, errorIndex, varBinds in iterator:
    
    if errorIndication:
        print(errorIndication)
        break

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))