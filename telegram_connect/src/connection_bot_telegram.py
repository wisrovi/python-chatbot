from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from files import writeSession, getLog
from config.config_bot import TOKEN_TELEGRAM
import processor


def start(update, context):
    context.bot.send_message(update.message.chat_id, "Bienvenido")


def mensaje_nocomando(update, context):
    cid = update.message.chat_id # obtengo el id_usuario
    question_user = update.message.text # obtengo el mensaje del usuario
    
    old_log = getLog(cid) # miro si hay un log previo cargado en cache, sino creo el cache para este usuario        
    old_log = "" if old_log is None else old_log  # si no hay log previo, lo inicializo en vacio
    old_log += f"Person: {question_user} \n" # agrego el mensaje del usuario al log

    answer = processor.chatbot_response(question_user) # envio el mensaje al chatbot y obtengo la respuesta
    
    new_log = old_log + f"Bot: {answer} \n" # concateno el log anterior con la nueva respuesta
    writeSession(cid, new_log) # guardo el cache para este usuario
    
    update.message.reply_text(answer) # respondo al usuario


if __name__=="__main__":
    print("Chatbot iniciado.")

    updater = Updater(TOKEN_TELEGRAM, use_context=True)
    dp=updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))    # respuesta al comando /start
    dp.add_handler(MessageHandler(Filters.text, mensaje_nocomando)) # respuesta a los comentarios del usuario
    
    updater.start_polling()    
    updater.idle()