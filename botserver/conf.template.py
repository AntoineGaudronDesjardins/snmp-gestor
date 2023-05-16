######################################### SNMP V3 CONFIGURATION #########################################
## Available authentication protocols:
from pysnmp.hlapi import usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol, usmHMAC128SHA224AuthProtocol, usmHMAC192SHA256AuthProtocol, usmHMAC256SHA384AuthProtocol, usmHMAC384SHA512AuthProtocol, usmNoAuthProtocol
## Available privacy protocols:
from pysnmp.hlapi import usmDESPrivProtocol, usm3DESEDEPrivProtocol, usmAesCfb128Protocol, usmAesCfb192Protocol, usmAesCfb256Protocol, usmNoPrivProtocol

switchConfig = {
    "ip": "XX.XX.XX.XX",
    "credentials": {
        "username" : {
            "authKey": "password",
            "authProtocol": usmHMACSHAAuthProtocol,
            "privKey": "password",
            "privProtocol": usmAesCfb128Protocol,
        },
    },
}

routerConfig = {
    "ip": "XX.XX.XX.XX",
    "community": "public",
}

finaldeviceConfig = {
    "ip": "XX.XX.XX.XX",
}

###################################### TELEGRAM BOT CONFIGURATION #######################################
TOKEN = "0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CHAN_ID = "XXXXXXXXXX"
