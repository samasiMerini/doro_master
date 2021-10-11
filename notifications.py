import telegram
from telegram.ext import *
import requests

import api
updater = Updater(token=api.APKI_TELEGRAM, use_context=True)
dispatcher = updater.dispatcher



def handle_message(update, message):
    text = str(update.message.text).lower()

    # Bot response
    update.message.reply_text(message)
    


def sendMessage(message):
    url = "https://api.telegram.org/bot"+api.APKI_TELEGRAM+"/sendMessage?chat_id="+api.CHAT_ID+"&parse_mode=Markdown&text="+message
    response = requests.get(url)
    return response.json()
    
