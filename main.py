from modules.utils import TrapListener
from modules.devices import Switch
from time import sleep


def main():
    print("Starting app...")
    switch = Switch('192.168.31.12')
    trapReceiver = TrapListener()
    trapReceiver.start()
    print(switch.getGlobalInfo())
    print(switch.setContact("antgau@alum.us.es"))
    print(switch.setLocation("2 planta - Sevilla"))
    print(switch.getGlobalInfo())
    sleep(4)
    trapReceiver.stop()
    sleep(2)
    trapReceiver.join()


if __name__ == "__main__":
    main()
