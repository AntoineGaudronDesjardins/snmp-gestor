from modules.snmp import ManagedNode, MibNode
from threading import Thread
from time import sleep


class Equipo(ManagedNode, Thread):
    def __init__(self, ipAddress):
        Thread.__init__(self)
        ManagedNode.__init__(self, ipAddress)
        self.__name__ = 'Equipo'


    ##################################################################################################
    ####################################### Triggers handlers ########################################
    ##################################################################################################
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
        self.triggersState = { 'ssh_sessions': True, 'num_apps_installed': True, 'shadow_size': True, 'failed_attempts': True }

        ssh_sessions = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull',"ssh_sessions")).get()
        num_apps_installed = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "num_apps_installed")).get()
        shadow_size = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "shadow_size")).get()
        failed_attempts = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "failed_attempts")).get()
        
        history = {
            'ssh_sessions': ssh_sessions.value,
            'num_apps_installed': num_apps_installed.value,
            'shadow_size': shadow_size.value,
            'failed_attempts': failed_attempts.value,
        }
        
        while True:
            ssh_sessions.get()
            num_apps_installed.get()
            shadow_size.get()
            failed_attempts.get()

            if self.triggersState['ssh_sessions'] and history['ssh_sessions'] < ssh_sessions.value:
                title = 'Nueva sesion SSH'
                desc = f'Una nueva sesion SSH (actualmente {ssh_sessions.values} activa{"s" if ssh_sessions.values > 1 else ""}) ha sido detectada en el equipo.'
                self.triggerAlert(title, desc)

            if self.triggersState['num_apps_installed'] and history['num_apps_installed'] < num_apps_installed.value:
                title = 'Nuevo software instalado'
                desc = f'Un nuevo software ha sido detectado en el equipo ({num_apps_installed.value} aplicacion{"es" if num_apps_installed.value > 1 else ""} detectadas)'
                self.triggerAlert(title, desc)

            if self.triggersState['shadow_size'] and history['shadow_size'] != shadow_size.value:
                title = 'Fichero "shadow" modificado'
                desc = f'Se ha observado un {"incremento" if history["shadow_size"] < shadow_size.value else "decremento"} del tamano del fichero "Shadow" en el equipo.'
                self.triggerAlert(title, desc)

            if self.triggersState['failed_attempts'] and history['failed_attempts'] != failed_attempts.value:
                title = 'Fracaso de autenticacion'
                desc = f'Un intento fallado de autenticacion al equipo ha sido detectado ({failed_attempts.values} desde el incio del sistema).'
                self.triggerAlert(title, desc)
            
            history = {
                'ssh_sessions': ssh_sessions.value,
                'num_apps_installed': num_apps_installed.value,
                'shadow_size': shadow_size.value,
                'failed_attempts': failed_attempts.value,
            }
            
            sleep(5)

    
