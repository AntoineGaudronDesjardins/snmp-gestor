# -*- coding: utf-8 -*-
import telegram
from telegram.ext import Updater, CommandHandler
import time
from modules.devices import Equipo

equipo = Equipo('172.20.10.3')

bot = telegram.Bot(token='6000262681:AAFxQSzgxUFHZF9mvcjI4gumFfS6qbD1wjM')

chat_id = '306898732'
def handle_command(update, context):
    """Maneja los comandos que llegan al bot"""
    command = update.message.text
    chat_id = update.message.chat_id
    if command.startswith('/getHealthMetrics'):
        #oid = command.split(' ')[1]
        #value = equipo.snmpEngine.get('SNMPv2-MIB', oid, format='pretty')
        value = equipo.getHealthMetrics(format="pretty")
        message = f"\nValor: {value}"
        bot.send_message(chat_id=chat_id, text=message)
    elif command == '/clear':
        clear_chat()


def clear_chat():
    """Borra todos los mensajes del chat"""
    messages = bot.get_updates()
    for msg in messages:
        chat_id = msg.message.chat_id
        message_id = msg.message.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)

# Valores iniciales
ssh_sessions_old = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull',"ssh_sessions", format="pretty")
num_apps_installed_old = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "num_apps_installed", format = "pretty")
shadow_size_old = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "shadow_size", format="pretty")
failed_attempts_old = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "failed_attempts", format="pretty")
updater = Updater(token='6000262681:AAFxQSzgxUFHZF9mvcjI4gumFfS6qbD1wjM', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("getHealthMetrics", handle_command))
dispatcher.add_handler(CommandHandler("clear", handle_command))


while True:
    
    # Configuración de handlers para manejar los comandos que lleguen al bot
    
    updater.start_polling()
    
    # Obtener nuevos valores
    ssh_sessions = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull',"ssh_sessions", format="pretty")
    num_apps_installed = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "num_apps_installed", format = "pretty")
    shadow_size = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "shadow_size", format="pretty")
    failed_attempts = equipo.snmpEngine.get('NET-SNMP-EXTEND-MIB', 'nsExtendOutputFull', "failed_attempts", format="pretty")

    # Verificar si los valores han cambiado
    if ssh_sessions != ssh_sessions_old or num_apps_installed != num_apps_installed_old or shadow_size != shadow_size_old or failed_attempts != failed_attempts_old:
        # Crear mensaje con los nuevos valores
        message = f"ssh_sessions: {ssh_sessions}\nnum_apps_installed: {num_apps_installed}\nshadow_size: {shadow_size}\nfailed_attempts: {failed_attempts}"
        # Enviar mensaje
        bot.send_message(chat_id=chat_id, text=message)
        # Actualizar valores antiguos
        ssh_sessions_old = ssh_sessions
        num_apps_installed_old = num_apps_installed
        shadow_size_old = shadow_size
        failed_attempts_old = failed_attempts
        

    # Esperar 5 segundos para la siguiente iteración
    time.sleep(1)
