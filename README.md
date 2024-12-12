# Apolo

![Logo](https://github.com/ddoyaguez/apolo-telegram-bot/blob/master/apolo_logo.png?raw=true)

This is Apolo. A self-hostable Telegram bot to download Youtube videos to MP3 over Telegram.

## Requirements
<ul>
    <li>Python >= 3.11</li>
    <li>ffmpeg</li>
    <li>firefox</li>
    <li>pip</li>
    <li>All stated on requirements.txt</li>
</ul>


## Features
<ul>
    <li>Uses yt-dlp</li>
    <li>Easy configuration via toml file</li>
    <li>~200 SLOC</li>
</ul>

## Configuration
Example config.toml:

```
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
msg_start = "I'm Apolo, I download music from Youtube, copy me a link and I will send you the MP3"
msg_url_list = ["Give me a second", "Let's go", "Copied, it won't take long", "On my way", "Downloading"]
msg_finished = ["Done, here it goes"]
```
<ul>
    <li>Apolo will randomly rotate from the msg lists, because why not</li>
    <li>You can put config.toml in the following locations:</li>
    <ul>
        <li>/opt/apolo-telegram-bot/config.toml</li>
        <li>/opt/apolo/config.toml</li>
        <li>/etc/apolo-telegram-bot/config.toml'</li>
        <li>~/apolo/apolo-telegram-bot/config.toml</li>
        <li>~/apolo/config.toml</li>
        <li>../config.toml'</li>
    </ul>
    <li>If you don't know or don't care then put it in the first option</li>
</ul>

Example systemd unit apolo.service file:
$ cat /etc/systemd/system/apolo.service
```
[Unit]
Description=Apolo Telegram Bot
After=network.target

[Service]
WorkingDirectory=/home/YOUR_NON_ROOT_USER/apolo
ExecStart=/home/YOUR_NON_ROOT_USER/VENVS/apolo/bin/python /home/YOUR_NON_ROOT_USER/apolo/apolo-telegram-bot/main.py
Type=simple
KillMode=control-group
User=YOUR_NON_ROOT_USER
Restart=on-failure

[Install]
WantedBy=default.target

```


