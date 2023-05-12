from modules.devices import Switch, Router
from modules.snmp import TrapListener
from modules.bot import Bot
from conf import TOKEN, switchConfig, routerConfig


def main():
    print("Starting app...")
    # Declare monitored devices
    router = Router(routerConfig['ip'], routerConfig['community'])
    # switch = Switch(switchConfig['ip'])
    # switch.resetTrapConfig()
    # Initalize bot
    bot = Bot(TOKEN)
    bot.addMonitoredDevices(router) #, switch)
    # Give bot reference for alerting
    # trapListener = TrapListener(bot=bot)
    router.registerBot(bot)
    # Launch trap listener and device pulling
    # trapListener.start()
    router.start()
    # trapListener.join()
    router.join()


if __name__ == "__main__":
    main()
