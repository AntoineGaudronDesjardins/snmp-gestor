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


def formatter(mibViewController, varBinds, format: str):
    if (not format) or ((not ":" in format) and (not "," in format)):
        return varBinds
    
    formatted = dict() if ":" in format else list()
    for inst, val in varBinds:
        instOID, instPretty = str(inst), inst.prettyPrint()
        instMib, instSymbol, instIndex = getMibSymbol(mibViewController, instOID)
        instIndex = [str(x) for x in instIndex]
        if isinstance(val, ObjectIdentity):
            valOID, valPretty = str(val), val.prettyPrint()
            valMib, valSymbol, valIndex = getMibSymbol(mibViewController, valOID)
            valIndex = [str(x) for x in valIndex]
        else:
            valOID = valMib = valSymbol = valIndex = valPretty = val.prettyPrint()

        special_key_words = { "inst": inst, "val": val }
        key_words = { "instOID": instOID, "instMib": instMib, "instSymbol": instSymbol, "instIndex": instIndex, "instPretty": instPretty,
                     "valOID": valOID, "valMib": valMib, "valSymbol": valSymbol, "valIndex": valIndex, "valPretty": valPretty }

        if ":" in format:
            key_pattern, value_pattern = format.split(':')
        else:
            key_pattern, value_pattern = format.split(',')
            
        if key_pattern in special_key_words:
            key_pattern = special_key_words[key_pattern]
        if key_pattern in key_words:
            key_pattern = key_words[key_pattern]
            
        if value_pattern in special_key_words:
            value_pattern = special_key_words[value_pattern]
        if value_pattern in key_words:
            value_pattern = key_words[value_pattern]

        for key, val in key_words.items():
            if isinstance(key_pattern, str):
                key_pattern = key_pattern.replace(key, str(val))
            if isinstance(value_pattern, str):
                value_pattern = value_pattern.replace(key, str(val))

        if ":" in format:
            formatted[key_pattern] = value_pattern
        else:
            formatted.append((key_pattern, value_pattern))

    return formatted
