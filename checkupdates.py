import requests
import subprocess
import sys
from datetime import date
import config
from telegram import Bot
import asyncio



async def update():
    config.read_config()

    package = 'yt-dlp'
    response = requests.get(f'https://pypi.org/pypi/{package}/json')
    latest_version = response.json()['info']['version']

    result = subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(package)], capture_output=True, text=True)
    current_version = ""
    if result.returncode == 0:
        l = list(filter(lambda line: line.startswith('Version:'), result.stdout.splitlines()))
        if len(l) > 0: current_version = l[0].split(":")[1].strip()

    result_subject = f"Actualización de {package} el {str(date.today())}"
    result_message = result_subject + "\n"

    result_message = result_message + (f"latest_version = {latest_version}") + "\n"
    result_message = result_message + (f"current_version = {current_version}") + "\n"
    if latest_version != current_version:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '{}'.format(package)], capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout != None:
                result_message += f"\n-------{config.CONFIG_DATA.get('msg_updateresult')}-------\n" + result.stdout + f"\n------{config.CONFIG_DATA.get('msg_updateendresult')}----\n"
            elif result.stderr != None:
                result_message += f"\n-------{config.CONFIG_DATA.get('msg_updateresult')}-------\n" + result.stderr + f"\n------{config.CONFIG_DATA.get('msg_updateendresult')}----\n"
            else:
                result_message = "Comprobado que no hay actualizaciones"
    chatadmin = None
    with open(str(config.CONFIG_DATA.get('path_chatadmin'))) as f:
        lines = f.readlines()
        if len(lines) > 0:
            chatadmin = int(lines[0].strip())
    bot = Bot(token=config.CONFIG_DATA.get('telegram_token'))
    await bot.send_message(chat_id=chatadmin, text=result_message)

asyncio.run(update())
        