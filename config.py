import tomllib
import os

CONFIG_PATHS = [
    '/etc/apolo-telegram-bot/config.toml',
    '/opt/apolo-telegram-bot/config.toml',
    '/opt/apolo/config.toml',
    '~/apolo/apolo-telegram-bot/config.toml',
    '~/apolo/config.toml',
    '../config.toml'
]

CONFIG_DATA = {}

def read_config():
    print("Reading config",flush=True)
    for CONFIG_PATH in CONFIG_PATHS:
        if os.path.isfile(CONFIG_PATH):
            print("Found {}".format(CONFIG_PATH), flush=True)
            global CONFIG_DATA
            CONFIG_DATA = read_config_file(CONFIG_PATH)
            return
        else:
            continue
    print("Error: Couldn't find any config.toml file", flush=True)
    exit(1)

def read_config_file(config_file_path):
    with open(config_file_path, "rb") as f:
        return tomllib.load(f)