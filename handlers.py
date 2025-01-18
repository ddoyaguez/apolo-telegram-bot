from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler
import random

import config
import download

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_start = config.CONFIG_DATA.get('msg_start')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_start)

async def setadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_user = config.CONFIG_DATA.get('admin_user')
    path_chatadmin = config.CONFIG_DATA.get('path_chatadmin')
    if int(admin_user) == update.effective_user.id:
        with open(path_chatadmin, 'w') as f:
            msg_setadmin_list = config.CONFIG_DATA.get('msg_setadmin_ok')
            msg_setadmin = random.choice(msg_setadmin_list)
            f.write(str(update.effective_chat.id))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_setadmin)
    else:
        msg_setadmin_list = config.CONFIG_DATA.get('msg_setadmin_na')
        msg_setadmin = random.choice(msg_setadmin_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_setadmin)

async def url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_url_list = config.CONFIG_DATA.get('msg_url_list')
    msg_url = random.choice(msg_url_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_url)
    download.download(update, context)

def add_handlers(application):
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    setadmin_handler = CommandHandler('setadmin', setadmin)
    application.add_handler(setadmin_handler)

    url_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), url)
    application.add_handler(url_handler)