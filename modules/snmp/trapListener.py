from modules.utils import createMibViewController

from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.smi.rfc1902 import ObjectIdentity
from pyasn1.codec.ber import decoder
from pyasn1.type.univ import ObjectIdentifier
from pysnmp.proto import api
from threading import Thread


class TrapListener(Thread):
    mibViewController = createMibViewController()

    def __init__(self, callback=None):
        Thread.__init__(self)
        self.transportDispatcher = AsyncoreDispatcher()
        if not callback:
            callback = TrapListener.callbackFunction
        self.transportDispatcher.registerRecvCbFun(callback)
        # In windows, set the server address as '' instead of 'localhost'
        transportAddress = udp.UdpSocketTransport().openServerMode(('', 162))
        self.transportDispatcher.registerTransport(udp.domainName, transportAddress)

    def run(self):
        print(f"Listening traps on port 162")

        self.transportDispatcher.jobStarted(1)
        try:
            # Dispatcher will not finish until job#1 finish
            self.transportDispatcher.runDispatcher()
        finally:
            self.transportDispatcher.closeDispatcher()

        print("Trap listener stopped")


    def stop(self):
        self.transportDispatcher.jobFinished(1)


    def callbackFunction(transportDispatcher, transportDomain, transportAddress, wholeMsg):

        while wholeMsg:

            msgVersion = int(api.decodeMessageVersion(wholeMsg))
            if msgVersion in api.protoModules:
                pMod = api.protoModules[msgVersion]
            else:
                print('Unsupported SNMP version %s' % msgVersion)
                return

            reqMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=pMod.Message())

            print('Notification message from %s:%s: ' %
                  (transportDomain, transportAddress))

            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVersion == api.protoVersion1:
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

                mibViewController = TrapListener.mibViewController
                for oid, val in varBinds:
                    oid = ObjectIdentity(oid)
                    oid.resolveWithMib(mibViewController)
                    if isinstance(val, ObjectIdentifier):
                        val = ObjectIdentity(val)
                        val.resolveWithMib(mibViewController)
                    print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

        return wholeMsg
