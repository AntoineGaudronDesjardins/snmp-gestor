from telepot import Bot as TelegramBot, glance, message_identifier
from telepot.loop import MessageLoop
from telepot.helper import Answerer
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from time import sleep

from modules.utils import createMibViewController, escapeChars


class Bot(Thread):
    def __init__(self, TOKEN, chanID='1911648518'):
        Thread.__init__(self)
        self.bot = TelegramBot(TOKEN)
        self.answerer = Answerer(self.bot)
        self.devices = dict()
        self.mibResolver = createMibViewController()
        self.chanID = chanID

        handlers = {
            'chat': lambda msg : self.handleMessage(msg),
            'callback_query': lambda msg : self.handleCallback(msg),
        }
        MessageLoop(self.bot, handlers).run_as_thread()

    
    def addMonitoredDevices(self, *devices):
        for device in devices:
            self.devices[device.ipAddress] = device

    
    def forwardTrap(self, ipAddress, varBinds):
        if ipAddress in self.devices:
            if self.devices[ipAddress].name:
                name = self.devices[ipAddress].name
            else:
                name = "sin nombre"
        else:
            name = "desconocido"
        name = escapeChars(name)
        ipAddress = escapeChars(ipAddress)
        data = "\n".join([varBind.print() for varBind in varBinds])
        data = escapeChars(data)
        msg = f'*Alerta de "{name}" \({ipAddress}\)*: \n\n{data}'

        self.bot.sendMessage(self.chanID, msg, parse_mode='MarkdownV2')

    
    ######################################################################################
    ################################ Interaction methods #################################
    ######################################################################################

    def handleMessage(self, msg):
        content_type, chat_type, chat_id = glance(msg)
        
        if msg['entities'][0]['type'] == 'bot_command':
            cmd, *args = msg['text'].split(' ')

            if cmd == '/interactive':
                keyBoard = [[InlineKeyboardButton(text=f"{device.name or 'sin nombre'}\n({ip})", callback_data=f"{device.__name__}&ip&{ip}")] for ip, device in self.devices.items()]
                keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
                self.bot.sendMessage(chat_id, 'Seleciona el equipo :', reply_markup=keyBoard)

            elif cmd == '/devices':
                devices = self._getDevices()
                self.bot.sendMessage(self.chanID, "\n".join([f"{name} : {ip}" for name, ip in devices]))

            elif cmd == '/triggers':
                

                # Send the table as a message using Markdown formatting
                # self.bot.sendMessage(chat_id, table, parse_mode='MarkdownV2')
                pass

            elif cmd == '/events':
                pass

            elif cmd == '/disable':
                pass

            elif cmd == '/enable':
                pass


    def handleCallback(self, msg):
        query_id, _, query_data = glance(msg, flavor='callback_query')
        msg_identifier = (msg['message']['chat']['id'], msg['message']['message_id'])
        query_data = query_data.split("&")

        if query_data[0] == 'devices':
            keyBoard = [[InlineKeyboardButton(text=f"{device.name or 'sin nombre'}\n({ip})", callback_data=f"{device.__name__}&ip&{ip}")] for ip, device in self.devices]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
            self.bot.editMessageText(msg_identifier, 'Seleciona el equipo :', reply_markup=keyBoard)

        if query_data[0] == 'Switch':
            self.switchHandler(msg_identifier, query_id, query_data[1:])

    
    ######################################################################################
    ############################## Device specific methods ###############################
    ######################################################################################
    def switchHandler(self, msg_identifier, query_id, query_data):

        if query_data[0] == 'ip':
            ip = query_data[1]
            keyBoard = [
                [InlineKeyboardButton(text='Informacion global', callback_data=f'Switch&info&{ip}')],
                [InlineKeyboardButton(text='Metricas de estado', callback_data=f'Switch&health&{ip}')],
                [InlineKeyboardButton(text='Gestion de las alarmas', callback_data=f'Switch&alerts&{ip}')],
                [InlineKeyboardButton(text="<< volver", callback_data="devices")]
            ]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
            self.bot.editMessageText(msg_identifier, 'Que quieres hacer :', reply_markup=keyBoard)

        elif query_data[0] == 'info':
            ip = query_data[1]
            device = self.devices[ip]
            
            info = "\n".join(device.printGlobalInfo())
            info = escapeChars(info)
            ipAddr = escapeChars(ip)
            msg = f'*__Informacion de {ipAddr}__*: \n\n{info}'

            keyBoard = [[InlineKeyboardButton(text="<< volver", callback_data=f"Switch&ip&{ip}")]]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, msg, parse_mode='MarkdownV2', reply_markup=keyBoard)
            
        elif query_data[0] == "health":
            ip = query_data[1]
            device = self.devices[ip]
            
            metrics = "\n".join(device.printHealthMetrics())
            metrics = escapeChars(metrics, ignore="_")
            name = escapeChars(device.name)
            respText = f'*__Actividad de {name}__* \n\n{metrics}'

            keyBoard = [[InlineKeyboardButton(text="<< volver", callback_data=f"Switch&ip&{ip}")]]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, respText, parse_mode='MarkdownV2', reply_markup=keyBoard)

        elif query_data[0] == "alerts":
            ip = query_data[1]
            keyBoard = [
                [InlineKeyboardButton(text='Alarmas', callback_data=f'Switch&triggers&{ip}')],
                [InlineKeyboardButton(text='Eventos', callback_data=f'Switch&events&{ip}')],
                [InlineKeyboardButton(text="<< volver", callback_data=f"Switch&ip&{ip}")]
            ]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
            self.bot.editMessageText(msg_identifier, 'Que quieres gestionar :', reply_markup=keyBoard)

        elif query_data[0] == "triggers":
            ip = query_data[1]
            device = self.devices[ip]

            keyBoard = []
            triggers, indexes = device.getTriggers()
            for trigger, index in zip(triggers, indexes):
                keyBoard.append([InlineKeyboardButton(text=trigger, callback_data=f"Switch&trigger&{ip}&{index}")])
            keyBoard.append([InlineKeyboardButton(text="<< volver", callback_data=f'Switch&alerts&{ip}')])
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, "Selecciona una alarma", reply_markup=keyBoard)

        elif query_data[0] == "events":
            ip = query_data[1]
            device = self.devices[ip]

            keyBoard = []
            events, indexes = device.getEvents()
            for event, index in zip(events, indexes):
                keyBoard.append([InlineKeyboardButton(text=event, callback_data=f"Switch&event&{ip}&{index}")])
            keyBoard.append([InlineKeyboardButton(text="<< volver", callback_data=f'Switch&alerts&{ip}')])
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, "Selecciona una evento", reply_markup=keyBoard)

        elif query_data[0] == "trigger":
            ip = query_data[1]
            device = self.devices[ip]
            index = query_data[2]
            if len(query_data) > 3:
                if query_data[3] == "True":
                    device.enableTrigger(index)
                    self.bot.answerCallbackQuery(query_id, text=f'Alarma activada')
                else:
                    device.disableTrigger(index)
                    self.bot.answerCallbackQuery(query_id, text=f'Alarma desactivada')

            trigger, enabled = device.getTrigger(index)
            trigger = escapeChars(trigger.print(), ignore="_")
            state = "desactivar" if enabled else "activar"
            
            keyBoard = [
                [InlineKeyboardButton(text=state, callback_data=f"Switch&trigger&{ip}&{index}&{not enabled}")],
                [InlineKeyboardButton(text="<< volver", callback_data=f"Switch&triggers&{ip}")],
            ]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, trigger, parse_mode='MarkdownV2', reply_markup=keyBoard)

        elif query_data[0] == "event":
            ip = query_data[1]
            device = self.devices[ip]
            index = query_data[2]
            if len(query_data) > 3:
                if query_data[3] == "True":
                    device.enableEvent(index)
                    self.bot.answerCallbackQuery(query_id, text=f'Evento activado')
                else:
                    device.disableEvent(index)
                    self.bot.answerCallbackQuery(query_id, text=f'Evento desactivado')

            event, enabled = device.getTrigger(index)
            event = escapeChars(event.print(), ignore="_")
            state = "desactivar" if enabled else "activar"
            
            keyBoard = [
                [InlineKeyboardButton(text=state, callback_data=f"Switch&event&{ip}&{index}&{not enabled}")],
                [InlineKeyboardButton(text="<< volver", callback_data=f"Switch&triggers&{ip}")],
            ]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, event, parse_mode='MarkdownV2', reply_markup=keyBoard)

    
    ######################################################################################
    ################################# Auxiliary methods ##################################
    ######################################################################################
    def run(self):
        # Keep the bot running
        while True:
            sleep(10)

    
    def _getDevices(self):
        return [(device.name if device.name else 'sin nombre', ip) for ip, device in self.devices.items()]