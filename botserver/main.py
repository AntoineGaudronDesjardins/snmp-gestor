from modules.devices import Switch, Router, Equipo
from modules.snmp import TrapListener
from modules.bot import Bot
from conf import TOKEN, CHAN_ID
from conf import switchConfig, routerConfig, finaldeviceConfig


def main():
    print("Starting app...")
    # Declare monitored devices
    router = Router(routerConfig['ip'], routerConfig['community'])
    switch = Switch(switchConfig['ip'], switchConfig["credentials"])
    equipo = Equipo(finaldeviceConfig['ip'])
    # Initalize bot
    bot = Bot(TOKEN, CHAN_ID)
    bot.addMonitoredDevices(equipo, router, switch)
    # Give bot reference for alerting
    trapListener = TrapListener(bot)
    router.registerBot(bot)
    equipo.registerBot(bot)
    # Launch trap listener and devices pulling
    # switch.resetTrapConfig()
    trapListener.start()
    equipo.start()
    router.start()
    # Wait for threads ending
    trapListener.join()
    equipo.join()
    router.join()


if __name__ == "__main__":
    main()
