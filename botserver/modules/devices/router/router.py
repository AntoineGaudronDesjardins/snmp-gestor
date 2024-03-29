from modules.snmp import ManagedNode, Table, MibNode
from threading import Thread
from time import sleep

class Router(ManagedNode, Thread):
    def __init__(self, ipAddress, community):
        Thread.__init__(self)
        ManagedNode.__init__(self, ipAddress, snmpWriteComunity=community)
        self.__name__ = 'Router'
        # MIKROTIK-MIB
        self.mtxrBuildTime = MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrBuildTime', 0)).get()
        self.mtxrLicSoftwareId = MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrLicSoftwareId', 0)).get()
        self.mtxrLicVersion = MibNode(self.snmpEngine, ('MIKROTIK-MIB', 'mtxrLicVersion', 0)).get()

    
    ##################################################################################################
    ##################################### INFORMACION DEL EQUIPO #####################################
    ##################################################################################################    
    def printGlobalInfo(self):
        globalInfo = ManagedNode.printGlobalInfo(self)
        
        if not self.mtxrBuildTime.ok:
            self.mtxrBuildTime.get()
        if self.mtxrBuildTime.ok:
            globalInfo.append(self.mtxrBuildTime.print())
        
        if not self.mtxrLicSoftwareId.ok:
            self.mtxrLicSoftwareId.get()
        if self.mtxrLicSoftwareId.ok:
            globalInfo.append(self.mtxrLicSoftwareId.print())
        
        if not self.mtxrLicVersion.ok:
            self.mtxrLicVersion.get()
        if self.mtxrLicVersion.ok:
            globalInfo.append(self.mtxrLicVersion.print())
        
        return globalInfo


    ##################################################################################################
    ####################################### Triggers handlers ########################################
    ##################################################################################################
    def getTriggersState(self):
        return self.triggersState
    

    def enableTrigger(self, trigger):
        if trigger in self.triggersState:
            self.triggersState[trigger] = True
            return True
        return False
    

    def disableTrigger(self, trigger):
        if trigger in self.triggersState:
            self.triggersState[trigger] = False
            return True
        return False
    

    ##################################################################################################
    ####################################### Monitoring thread ########################################
    ##################################################################################################
    def run(self):
        self.triggersState = { 'ifInOctets': True, 'ifOutOctets': True, 'ifInErrors': True, 'ifOutErrors': True, 'ifOperStatus': True }

        ifTable = Table(self.snmpEngine, 'IF-MIB', 'ifTable').pullData('ifIndex', 'ifInOctets', 'ifOutOctets', 'ifInErrors', 'ifOutErrors', 'ifOperStatus')
        ifMetrics = {
            IfIndex : {
                'ifInErrors': int(ifInErrors),
                'ifOutErrors': int(ifOutErrors),
                'ifOperStatus': ifOperStatus,
            } for IfIndex, _, _, ifInErrors, ifOutErrors, ifOperStatus in ifTable.values
        }
        
        while True:

            if ifTable.refresh().ok:
                for ifIndex, ifInOctets, ifOutOctets, ifInErrors, ifOutErrors, ifOperStatus in ifTable.values:

                    ##################################################################################################
                    ##################################### MONITOREO DEL TRÁFICO ######################################
                    ##################################################################################################
                    if self.triggersState['ifInOctets'] and (int(ifInOctets) > 100000000):
                        title = "Tráfico entrante masivo"
                        desc = f"El trafico entrante por el puerto {ifIndex} del equipo supera los 100MB (medido: {ifInOctets})"
                        self.triggerAlert(title, desc)
                    
                    if self.triggersState['ifOutOctets'] and (int(ifOutOctets) > 100000000):
                        title = "Tráfico saliente masivo"
                        desc = f"El trafico saliente por el puerto {ifIndex} del equipo supera los 100MB (medido: {ifOutOctets})"
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
                    
                    if self.triggersState['ifOutErrors'] and (ifMetrics[ifIndex]['ifOperStatus'] != ifOperStatus):
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
