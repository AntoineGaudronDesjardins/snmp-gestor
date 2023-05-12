from modules.snmp import ManagedNode, Table, MibNode
from threading import Thread
from time import sleep

class Router(ManagedNode, Thread):
    def __init__(self, ipAddress, community):
        Thread.__init__(self)
        ManagedNode.__init__(self, ipAddress, snmpWriteComunity=community)
        self.__name__ = 'Router'
    

    def registerBot(self, bot):
        self.bot = bot


    ##################################################################################################
    ####################################### Triggers handlers ########################################
    ##################################################################################################
    
    def triggerAlert(self, title, desc):
        self.bot.sendAlert(self.ipAddress, title, desc)
    

    def getTriggersState(self):
        return self.triggersState
    

    def enableTrigger(self, trigger):
        if trigger in self.triggersState:
            self.triggersState[trigger] = True
    

    def disableTrigger(self, trigger):
        if trigger in self.triggersState:
            self.triggersState[trigger] = False
    

    ##################################################################################################
    ####################################### Monitoring thread ########################################
    ##################################################################################################
    def run(self):
        self.triggersState = { 'ifInOctets': True, 'ifOutOctets': True, 'ifInErrors': True, 'ifOutErrors': True }
        tiempo_up = MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemUptime', 0))
        ifTable = Table(self.snmpEngine, 'IF-MIB', 'ifTable')
        ifMetrics = dict()
        while True:
            tiempo_up = tiempo_up.get()
            ifTable = ifTable.pullData('ifIndex', 'ifInOctets', 'ifOutOctets', 'ifInErrors', 'ifOutErrors', 'ifOperStatus')

            for ifIndex, ifInOctets, ifOutOctets, ifInErrors, ifOutErrors, ifOperStatus in ifTable.values:

                ##################################################################################################
                ##################################### MONITOREO DEL TRÁFICO ######################################
                ##################################################################################################
                if self.triggersState['ifInOctets'] and (int(ifInOctets) > 1000000):
                    title = "Tráfico entrante masivo"
                    desc = f"El trafico entrante por el puerto {ifIndex} del equipo supera los 1MB (medido: {ifInOctets})"
                    self.triggerAlert(title, desc)
                
                if self.triggersState['ifOutOctets'] and (int(ifOutOctets) > 1000000):
                    title = "Tráfico saliente masivo"
                    desc = f"El trafico saliente por el puerto {ifIndex} del equipo supera los 1MB (medido: {ifOutOctets})"
                    self.triggerAlert(title, desc)
                
                if self.triggersState['ifInErrors'] and (ifIndex in ifMetrics.keys()) and (int(ifInErrors) - ifMetrics[ifIndex]['ifInErrors'] > 0):
                    errors = int(ifInErrors) - ifMetrics[ifIndex]['ifInErrors']
                    title = "Tráfico entrante error"
                    desc = f"Se ha detectado {errors} error{'es' if errors > 1 else ''} en el trafico entrante por el puerto {ifIndex} del equipo."
                    self.triggerAlert(title, desc)
                
                if self.triggersState['ifOutErrors'] and (ifIndex in ifMetrics.keys()) and (int(ifOutErrors) - ifMetrics[ifIndex]['ifOutErrors'] > 0):
                    errors = int(ifOutErrors) - ifMetrics[ifIndex]['ifOutErrors']
                    title = "Tráfico saliente error"
                    desc = f"Se ha detectado {errors} error{'es' if errors > 1 else ''} en el trafico saliente por el puerto {ifIndex} del equipo."
                    self.triggerAlert(title, desc)
                
                if ifIndex in ifMetrics.keys() and ifMetrics[ifIndex]['ifOperStatus'] != ifOperStatus:
                    title = "Cambio de interfaz"
                    desc = f"La interfaz {ifIndex} ha pasado del estado {ifMetrics[ifIndex]['ifOperStatus']} al estado {ifOperStatus}"
                    self.triggerAlert(title, desc)
                

                ##################################################################################################
                ################################### GUARDA METRICAS PRECEDENTES ##################################
                ##################################################################################################                
                ifMetrics[ifIndex] = {
                    'ifInErrors': int(ifInErrors),
                    'ifOutErrors': int(ifOutErrors),
                    'ifOperStatus': ifOperStatus,
                }
            
            sleep(5)
    

    ##################################################################################################
    ##################################### INFORMACION DEL EQUIPO #####################################
    ##################################################################################################    
    def printGlobalInfo(self):
        globalInfo = ManagedNode.printGlobalInfo(self)
        # MIKROTIK-MIB
        globalInfo.append(MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrBuildTime', 0)).get().print())
        globalInfo.append(MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrLicSoftwareId', 0)).get().print())
        globalInfo.append(MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrLicVersion', 0)).get().print())
        return globalInfo
            
    
    def printHealthMetrics(self):
        healthMetrics = []
        # HOST-RESOURCES-MIB metrics
        healthMetrics.append(MibNode(self.snmpEngine, ('HOST-RESOURCES-MIB', 'hrSystemUptime', 0)).get().print())
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrStorageTable').pullData('hrStorageIndex', 'hrStorageUsed').print(index=False))
        healthMetrics.append(Table(self.snmpEngine, 'HOST-RESOURCES-MIB', 'hrProcessorTable').pullData('hrProcessorFrwID', 'hrProcessorLoad').print(index=False))
        # IF-MIB metrics
        healthMetrics.append(Table(self.snmpEngine, 'IF-MIB', 'ifTable').pullData('ifIndex', 'ifOperStatus', 'ifLastChange', 'ifOutOctets').print(index=False))
        return healthMetrics