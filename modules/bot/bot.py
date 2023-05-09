from telepot import Bot as TelegramBot, glance, message_identifier
from telepot.loop import MessageLoop
from telepot.helper import Answerer
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from threading import Thread
from time import sleep

from modules.utils import formatter, createMibViewController
from modules.snmp import Table, MibNode


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
        msgTemplate = 'Alerta de "{}" ({}): \n{}'
        varBinds = [f" {inst} = {val}" for inst, val in formatter(self.mibResolver, varBinds, format='instSymbol,valSymbol')]
        if ipAddress in self.devices:
            if self.devices[ipAddress].name:
                name = self.devices[ipAddress].name
            else:
                name = "sin nombre"
        else:
            name = "desconocido"
        self.bot.sendMessage(self.chanID, msgTemplate.format(name, ipAddress, "\n".join(varBinds)))

    
    ######################################################################################
    ################################ Interaction methods #################################
    ######################################################################################

    def handleMessage(self, msg):
        content_type, chat_type, chat_id = glance(msg)
        
        if msg['entities'][0]['type'] == 'bot_command':
            cmd, *args = msg['text'].split(' ')

            if cmd == '/interactive':
                devices = self._getDevices()
                keyBoard = [[InlineKeyboardButton(text=f"{name}\n({ip})", callback_data=f"ip&{ip}")] for name, ip in devices]
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
        query_id, from_id, query_data = glance(msg, flavor='callback_query')
        msg_identifier = (msg['message']['chat']['id'], msg['message']['message_id'])
        query_data = query_data.split("&")

        if query_data[0] == 'devices':
            devices = self._getDevices()
            keyBoard = [[InlineKeyboardButton(text=f"{name}\n({ip})", callback_data=f"ip&{ip}")] for name, ip in devices]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
            self.bot.editMessageText(msg_identifier, 'Seleciona el equipo :', reply_markup=keyBoard)

        elif query_data[0] == 'ip':
            ip = query_data[1]
            keyBoard = [
                [InlineKeyboardButton(text='Informacion global', callback_data=f'info&{ip}')],
                [InlineKeyboardButton(text='Metricas de estado', callback_data=f'health&{ip}')],
                [InlineKeyboardButton(text='Gestion de las alarmas', callback_data=f'alerts&{ip}')],
                [InlineKeyboardButton(text="<< volver", callback_data="devices")]
            ]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
            self.bot.editMessageText(msg_identifier, 'Que quieres hacer :', reply_markup=keyBoard)

        elif query_data[0] == 'info':
            ip = query_data[1]
            device = self.devices[ip]
            
            msgTemplate = 'Informacion de {} \n\n{}'
            metrics = device.getGlobalInfo()
            metrics = [f" {inst} = {val}" for inst, val in metrics.items()]

            keyBoard = [[InlineKeyboardButton(text="<< volver", callback_data=f"ip&{ip}")]]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, msgTemplate.format(ip, "\n".join(metrics)), reply_markup=keyBoard)
            
        elif query_data[0] == "health":
            ip = query_data[1]
            device = self.devices[ip]
            printableName = "\-".join(device.name.split("-"))
            
            respText = f'*__Actividad de {printableName}__* \n\n'
            metrics = device.getHealthMetrics()
            for obj in metrics.items():
                respText = respText + obj

            keyBoard = [[InlineKeyboardButton(text="<< volver", callback_data=f"ip&{ip}")]]
            keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)

            self.bot.editMessageText(msg_identifier, respText, parse_mode='MarkdownV2', reply_markup=keyBoard)


            pass
        # device = self.devices[query_data[1]]
        # keyBoard = [
        #     [InlineKeyboardButton(text='Metricas globales', callback_data='3&health')],
        #     [InlineKeyboardButton(text='Historico de alarmas', callback_data='3&alerts')],
        # ]
        # keyBoard = InlineKeyboardMarkup(inline_keyboard=keyBoard)
        # self.bot.editMessageReplyMarkup(msg_identifier, keyBoard)


        # self.bot.answerCallbackQuery(query_id, text=f'Got it ({query_data})')

    
    ######################################################################################
    ################################# Auxiliary methods ##################################
    ######################################################################################
    def run(self):
        # Keep the bot running
        while True:
            sleep(10)

    
    def _getDevices(self):
        return [(device.name if device.name else 'sin nombre', ip) for ip, device in self.devices.items()]