from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler
import random

import config
import download

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_start = config.CONFIG_DATA.get('msg_start')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_start)

async def url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_url_list = config.CONFIG_DATA.get('msg_url_list')
    msg_url = random.choice(msg_url_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_url)
    download.download(update, context)

def add_handlers(application):
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    url_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), url)
    application.add_handler(url_handler)