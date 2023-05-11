from modules.devices import Switch
from modules.snmp import TrapListener
from modules.bot import Bot
from conf import TOKEN


def main():
    print("Starting app...")
    # Declare monitored devices
    switch = Switch('192.168.31.10')
    # switch.resetTrapConfig()
    # Initalize bot
    bot = Bot(TOKEN)
    bot.addMonitoredDevices(switch)
    # Set up trap listener
    trapListener = TrapListener(bot=bot)
    trapListener.start()
    trapListener.join()


if __name__ == "__main__":
    main()
