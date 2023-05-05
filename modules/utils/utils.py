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


def formatter(mibViewController, varBinds, format):
    formatted = dict()
    for varBind in varBinds:
        name, value = varBind
        _, nameSymbol, _ = getMibSymbol(mibViewController, str(name))

        if format == "default":
            formatted[name] = value

        elif format == "pretty":
            formatted[name.prettyPrint()] = value.prettyPrint()

        elif format == "symbol":
            if isinstance(value, ObjectIdentity):
                _, valSymbol, _ = getMibSymbol(mibViewController, str(value))
                formatted[nameSymbol] = valSymbol
            else:
                formatted[nameSymbol] = value.prettyPrint()

        elif format == "valueOID":
            if isinstance(value, ObjectIdentity):
                formatted[nameSymbol] = str(value)
            else:
                formatted[nameSymbol] = value.prettyPrint()

        elif format == "keyOID":
            formatted[str(name)] = value

        elif format == "OID":
            if isinstance(value, ObjectIdentity):
                formatted[str(name)] = str(value)
            else:
                formatted[str(name)] = value.prettyPrint()
            
        else:
            return varBinds
    return formatted
