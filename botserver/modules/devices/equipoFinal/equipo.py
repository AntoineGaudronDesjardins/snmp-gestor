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
        self.triggersState = { 'ssh_sessions': True, 'num_apps_installed': True, 'shadow_size': True, 'failed_attempts': True }

        ssh_sessions = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "ssh_sessions")).get()
        num_apps_installed = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "num_apps_installed")).get()
        shadow_size = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "shadow_size")).get()
        failed_attempts = MibNode(self.snmpEngine, ('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "failed_attempts")).get()
        
        history = {
            'ssh_sessions': ssh_sessions.value if ssh_sessions.ok else 0,
            'num_apps_installed': num_apps_installed.value if num_apps_installed.ok else 0,
            'shadow_size': shadow_size.value if shadow_size.ok else 0,
            'failed_attempts': failed_attempts.value if failed_attempts.ok and isinstance(failed_attempts.value, int) else 0,
        }
        
        while True:
            
            if self.triggersState['ssh_sessions']:
                ssh_sessions.get()
                if ssh_sessions.ok and history['ssh_sessions'] < ssh_sessions.value:
                    history['ssh_sessions'] = ssh_sessions.value
                    title = 'Nueva sesion SSH'
                    desc = f'Una nueva sesion SSH (actualmente {ssh_sessions.value} activa{"s" if ssh_sessions.value > 1 else ""}) ha sido detectada en el equipo.'
                    self.triggerAlert(title, desc)

            if self.triggersState['num_apps_installed']:
                num_apps_installed.get()
                if num_apps_installed.ok and history['num_apps_installed'] < num_apps_installed.value:
                    history['num_apps_installed'] = num_apps_installed.value
                    title = 'Nuevo software instalado'
                    desc = f'Un nuevo software ha sido detectado en el equipo ({num_apps_installed.value} aplicacion{"es" if num_apps_installed.value > 1 else ""} detectadas)'
                    self.triggerAlert(title, desc)

            if self.triggersState['shadow_size']:
                shadow_size.get()
                if shadow_size.ok and history['shadow_size'] != shadow_size.value:
                    history['shadow_size'] = shadow_size.value
                    title = 'Fichero "shadow" modificado'
                    desc = f'Se ha observado un {"incremento" if history["shadow_size"] < shadow_size.value else "decremento"} del tamano del fichero "Shadow" en el equipo.'
                    self.triggerAlert(title, desc)

            if self.triggersState['failed_attempts']:
                failed_attempts.get()
                failed_attempts_value = failed_attempts.value if isinstance(failed_attempts.value, int) else 0
                if failed_attempts.ok and history['failed_attempts'] != failed_attempts_value:
                    history['failed_attempts'] = failed_attempts_value
                    title = 'Fracaso de autenticacion'
                    desc = f'Un intento fallado de autenticacion al equipo ha sido detectado ({failed_attempts_value} desde el incio del sistema).'
                    self.triggerAlert(title, desc)
            
            sleep(5)

    
