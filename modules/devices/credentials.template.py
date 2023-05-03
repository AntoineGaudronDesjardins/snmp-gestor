## Available authentication protocols:
from pysnmp.hlapi import usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol, usmHMAC128SHA224AuthProtocol, usmHMAC192SHA256AuthProtocol, usmHMAC256SHA384AuthProtocol, usmHMAC384SHA512AuthProtocol, usmNoAuthProtocol
## Available privacy protocols:
from pysnmp.hlapi import usmDESPrivProtocol, usm3DESEDEPrivProtocol, usmAesCfb128Protocol, usmAesCfb192Protocol, usmAesCfb256Protocol, usmNoPrivProtocol

credentials = {
    "username" : {
        "authKey": "authenticationPassword",
        "authProtocol": usmHMACMD5AuthProtocol,
        "privKey": "privacyPassword",
        "privProtocol": usmDESPrivProtocol,
    },
}