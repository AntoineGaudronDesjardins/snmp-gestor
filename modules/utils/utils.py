from pysnmp.smi.builder import MibBuilder, DirMibSource
from pysnmp.smi.view import MibViewController
from pysnmp.smi.rfc1902 import ObjectIdentity
import os


def createMibViewController():
    mibBuilder = MibBuilder()
    mibBuilder.addMibSources(DirMibSource(os.path.join(os.getcwd(), 'mibs')))
    mibBuilder.loadModules('DISMAN-EVENT-MIB', 'HOST-RESOURCES-MIB', 'IF-MIB', 'IP-MIB', 'SNMPv2-MIB', 'TCP-MIB', 'UDP-MIB', 'NET-SNMP-MIB')
    mibViewController = MibViewController(mibBuilder)
    return mibViewController


def getOid(mibViewController, *args, stringify=False):
    oid = ObjectIdentity(*args)
    oid.resolveWithMib(mibViewController)
    res = oid.getOid()
    if stringify:
        res = str(res)
    return res


def getMibSymbol(mibViewController, oid):
    oid = ObjectIdentity(oid)
    oid.resolveWithMib(mibViewController)
    return oid.getMibSymbol()


def getMibLabel(mibViewController, oid):
    oid = ObjectIdentity(oid)
    oid.resolveWithMib(mibViewController)
    return oid.getLabel()


def getMibNode(mibViewController, oid):
    oid = ObjectIdentity(oid)
    oid.resolveWithMib(mibViewController)
    return oid.getMibNode()


def getTableColumns(mibViewController, mibName, tableName):
    tableOid = getOid(mibViewController, mibName, tableName)
    columns = []
    i = 0
    while True:
        i += 1
        _, column, args = getMibSymbol(mibViewController, f"{tableOid}.1.{i}")
        if args:
            break
        columns.append(column)
    return columns


def formatter(mibViewController, *varBinds, format="default"):
    formatted = dict()
    for varBind in varBinds:
        for name, value in varBind:
            _, nameSymbol, _ = getMibSymbol(mibViewController, str(name))

            if format == "default":
                formatted[name] = value

            elif format == "symbol":
                formatted[nameSymbol] = value

            elif format == "pretty":
                formatted[nameSymbol] = value.prettyPrint()

            elif format == "valueOID":
                if isinstance(value, ObjectIdentity):
                    formatted[nameSymbol] = str(value)
                else:
                    formatted[nameSymbol] = value.prettyPrint()

            elif format == "keyOID":
                formatted[str(name)] = value
                
            else:
                return varBinds
    return formatted
