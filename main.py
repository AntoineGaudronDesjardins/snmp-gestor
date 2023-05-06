from modules.devices import Switch
from modules.snmp import TrapListener
from modules.bot import Bot
from conf import TOKEN
from time import sleep


def main():
    print("Starting app...")
    # Declare monitored devices
    switch = Switch('192.168.31.10', name="switch - 2C")
    # Initalize bot and trap listener
    bot = Bot(TOKEN)
    bot.addMonitoredDevices(switch)
    trapListener = TrapListener(bot=bot)
    trapListener.start()
    trapListener.join()
    # switch.resetTrapConfig()
    # print(switch.getTriggers())
    # print(switch.getEvents())
    # print(switch.snmpEngine.walkByOID("1.3.6.1.2.1.2", format="instSymbol:valPretty"))
    # print(switch.snmpEngine.walk("SNMPv2-MIB", "system", format="instSymbol:valPretty"))
    # print(switch.getGlobalInfo(format="instPretty:valPretty"))
    # print(switch.getHealthMetrics(format="instPretty:valPretty"))
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', format='instPretty:valPretty'))
    # print(switch.snmpEngine.getByOID("1.3.6.1.2.1.25.2.3.1.6.1", format="instPretty:valPretty"))
    # while True:
    #     print(switch.snmpEngine.get('HOST-RESOURCES-MIB', 'hrSystemUptime', 0, format="instPretty:valPretty"))
    #     print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'sysUpTimeInstance', format="instPretty:valPretty"))
    #     print(switch.snmpEngine.getTable('HOST-RESOURCES-MIB', 'hrProcessorTable', 'hrProcessorFrwID', 'hrProcessorLoad', format="instPretty:valPretty"))
    #     print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteResourceSampleInstances', 0, format="instPretty:valPretty"))
    #     print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteTriggerFailures', 0, format="instPretty:valPretty"))
    #     sleep(2)
    # print(switch.snmpEngine.getTable('IF-MIB', 'ifTable', format="instPretty:valPretty"))
    # print(switch.snmpEngine.get('DISMAN-EVENT-MIB', 'mteObjectsID', 'antoine','healthGroup', '1', format="instPretty:valPretty"))
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', format="instPretty:valPretty")['mteObjectsTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', startIndex=['antoine','healthGroup', '1'], format="instPretty:valPretty")['mteObjectsTable'])
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', startIndex=['antoine','MachineTooBusy'], maxRepetitions=1, format="instPretty:valPretty")['mteTriggerTable'])
    
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerTable', format="instPretty:valPretty")['mteTriggerTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerDeltaTable', format="instPretty:valPretty")['mteTriggerDeltaTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerExistenceTable', format="instPretty:valPretty")['mteTriggerExistenceTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerBooleanTable', format="instPretty:valPretty")['mteTriggerBooleanTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteTriggerThresholdTable', format="instPretty:valPretty")['mteTriggerThresholdTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', format="instPretty:valPretty")['mteObjectsTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventTable', format="instSymbol:valPretty")['mteEventTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventNotificationTable', format="instPretty:valPretty")['mteEventNotificationTable'])
    # print('\n')
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventSetTable', format="instPretty:valPretty")['mteEventSetTable'])

    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteEventNotificationTable', format="instPretty:valPretty")['mteEventNotificationTable'])
    # print(switch.setContact("antgau@alum.us.es"))
    # print(switch.setLocation("2 planta - Sevilla"))
    # print(switch.getGlobalInfo(format="OID"))
    # sleep(4)
    # print(switch.snmpEngine.getTable('DISMAN-EVENT-MIB', 'mteObjectsTable', startIndex=['antoine','healthGroup', '1'], format="instPretty:valPretty")['mteObjectsTable'])
    # trapListener.stop()
    # sleep(2)
    # trapListener.join()


if __name__ == "__main__":
    main()
