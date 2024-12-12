from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ContextTypes

import asyncio
import config

import os

u: Update = None
c: ContextTypes.DEFAULT_TYPE = None

async def _send_and_remove(downloaded_filename):
    # print("_send_and_remove\n", flush=True)
    global u
    global c
    with open("./" + downloaded_filename, "rb") as f:
        # print("awaiting message send\n", flush=True)
        await c.bot.send_document(chat_id=u.effective_chat.id, document=f)
    os.remove("./" + downloaded_filename)
    # print("_download_hook complete\n", flush=True)
    u = None
    c = None

def _download_hook(d):
    # print("_download_hook\n", flush=True)
    global u
    global c
    if d['status'] == 'finished' and d['postprocessor'] == 'MoveFiles':
        # import pdb; pdb.set_trace()
        # print("_download_hook entered status finished")
        # msg_finished = config.CONFIG_DATA.get('msg_finished')
        downloaded_filename_original = d['info_dict']['filename']
        downloaded_filename = downloaded_filename_original.replace(".m4a", ".mp3")
        # check if mp3 file exists
        if not os.path.exists(downloaded_filename):
            # print(downloaded_filename + " does not exist yet, returning\n", flush=True)
            return
        # check if m4a file exists
        if os.path.exists(downloaded_filename_original) and os.path.exists(downloaded_filename):
            # print(downloaded_filename_original + " still exists, returning")
            return
        print("downloaded_filename = " + downloaded_filename + "\n", flush=True)
        try:
            # print("loop detected\n", flush=True)
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            # print("no loop detected\n", flush=True)
            loop = None

        if loop and loop.is_running():
            # print("creating task\n", flush=True)
            tsk = loop.create_task(_send_and_remove(downloaded_filename))
        else:
            # print("asyncio run\n", flush=True)
            asyncio.run(_send_and_remove(downloaded_filename))
        
def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global u
    global c
    u = update
    c = context
    # print("download\n", flush=True)
    save_path = str(update.effective_chat.id) + "/%(title)s.%(ext)s"
    urls = update.effective_message.text.split("\n")
    urls = list(filter(lambda x: x.startswith("https://"), urls))
    ydl_opts = {
        'verbose': True,
        'cookiesfrombrowser': ('firefox',),
        'outtmpl': save_path,
        'format': 'm4a/bestaudio/best',
        'writethumbnail': 'true',
        'embedthumbnail': 'true',
        'postprocessors': [
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True
            },
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            },
            {
                'key': 'EmbedThumbnail',
                # 'already_have_thumbnail': False
            }
            ],
        'postprocessor_hooks': [_download_hook]
    }

    # if os.path.exists(config.CONFIG_DATA['cookiefile']):
    #     print("adding cookiefile to opts")
    #     ydl_opts['cookiefile'] = config.CONFIG_DATA['cookiefile']

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download(urls)