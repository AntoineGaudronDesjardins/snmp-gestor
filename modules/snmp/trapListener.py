from modules.utils import createMibViewController
from modules.snmp.mibNode import MibNode
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber.decoder import decode
from pysnmp.proto.api import decodeMessageVersion, protoModules, protoVersion1
from threading import Thread


class TrapListener(Thread):
    mibViewController = createMibViewController()

    def __init__(self, callback=None, bot=None):
        Thread.__init__(self)
        if not callback:
            callback = self.callbackFunction
        # In windows, set the server address as '' instead of 'localhost'
        transportAddress = udp.UdpSocketTransport().openServerMode(('', 162))

        self.bot = bot
        self.transportDispatcher = AsyncoreDispatcher()
        self.transportDispatcher.registerRecvCbFun(callback)
        self.transportDispatcher.registerTransport(udp.domainName, transportAddress)

    def run(self):
        print(f"Listening traps on port 162")

        self.transportDispatcher.jobStarted(1)
        try:
            self.transportDispatcher.runDispatcher()
        finally:
            self.transportDispatcher.closeDispatcher()

        print("Trap listener stopped")


    def stop(self):
        self.transportDispatcher.jobFinished(1)


    def callbackFunction(self, _, transportDomain, transportAddress, msg):

        while msg:

            msgVersion = int(decodeMessageVersion(msg))
            if msgVersion in protoModules:
                pMod = protoModules[msgVersion]
            else:
                print('Unsupported SNMP version %s' % msgVersion)
                return

            reqMsg, msg = decode(msg, asn1Spec=pMod.Message())

            print('\nNotification message from %s:%s: ' %
                  (transportDomain, transportAddress))

            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVersion == protoVersion1:
                    print('Enterprise: %s' %
                          (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                    print('Agent Address: %s' %
                          (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                    print('Generic Trap: %s' %
                          (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                    print('Specific Trap: %s' %
                          (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                    print('Uptime: %s' %
                          (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                    varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                else:
                    varBinds = pMod.apiPDU.getVarBinds(reqPDU)

                print('Var-binds:')
                varBinds = [MibNode(None, ObjectType(ObjectIdentity(varBind[0]), varBind[1]), self.mibViewController) for varBind in varBinds]
                for varBind in varBinds:
                    print(varBind)
                print('\n')

                if self.bot:
                    self.bot.forwardTrap(transportAddress[0], varBinds)

        return msg
