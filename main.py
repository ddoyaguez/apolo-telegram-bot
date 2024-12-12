import config
import os

from handlers import add_handlers

from telegram.ext import ApplicationBuilder

if __name__ == '__main__':
    print("Apolo v0.1 started", flush=True)
    # Read config
    config.read_config()

    # Check cookie file exists and say it
    if os.path.exists(config.CONFIG_DATA['cookiefile']):
        print("- Cookie file found", flush=True)

    # Build Telegram Bot
    application = ApplicationBuilder().token(config.CONFIG_DATA.get('telegram_token')).build()

    # Add handlers
    add_handlers(application)

    # Main loop
    application.run_polling()