from modules.devices import Switch
from modules.snmp import TrapListener
from time import sleep


def main():
    print("Starting app...")
    trapListener = TrapListener()
    trapListener.start()
    switch = Switch('192.168.31.10')
    switch.initTraps()
    # print(switch.getGlobalInfo(format="pretty"))
    # print(switch.getHealthMetrics(format="pretty"))
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', format='keyOID'))
    while True:
        # print(switch.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemUptime', 0, format="pretty"))
        print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'sysUpTimeInstance', format="pretty"))
        print(switch.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrProcessorTable', 'hrProcessorFrwID', 'hrProcessorLoad', format="pretty"))
        print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteResourceSampleInstances', 0, format="pretty"))
        print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteTriggerFailures', 0, format="pretty"))
        sleep(2)
    # print(switch.snmpEngine.getTable('IF-MIB', 'ifTable', format="pretty"))
    # print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteObjectsID', 'antoine','healthGroup', '1', format="pretty"))
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', format="pretty")['mteObjectsTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', startIndex=['antoine','healthGroup', '1'], format="pretty")['mteObjectsTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', startIndex=['antoine','MachineTooBusy'], maxRepetitions=1, format="pretty")['mteTriggerTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerDeltaTable', format="pretty")['mteTriggerDeltaTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerExistenceTable', format="pretty")['mteTriggerExistenceTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerBooleanTable', format="pretty")['mteTriggerBooleanTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerThresholdTable', format="pretty")['mteTriggerThresholdTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', format="pretty")['mteObjectsTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventTable', format="symbol")['mteEventTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventNotificationTable', format="oid")['mteEventNotificationTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventNotificationTable', format="oid")['mteEventNotificationTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventSetTable', format="pretty")['mteEventSetTable'])
    # print(switch.setContact("antgau@alum.us.es"))
    # print(switch.setLocation("2 planta - Sevilla"))
    # print(switch.getGlobalInfo())
    # sleep(4)
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', startIndex=['antoine','healthGroup', '1'], format="pretty")['mteObjectsTable'])
    # trapListener.stop()
    # sleep(2)
    trapListener.join()


if __name__ == "__main__":
    main()
