import json
import os
import sys
from builtins import dict, open

CONFIG_PATH = "config.json"


def get_project_settings():
    if not os.path.isfile(CONFIG_PATH):
        print('A file with the name "config.json" was not found in the root directory')
        sys.exit(1)

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    settings = dict(
        MAIL_SERVER=config['MAIL_SERVER'],
        MAIL_PORT=config['MAIL_PORT'],
        MAIL_USERNAME=config['MAIL_USERNAME'],
        MAIL_PASSWORD=config['MAIL_PASSWORD'],
        MAIL_RECIPIENTS=config['MAIL_RECIPIENTS'],
        SEND_FILE_MAX_AGE_DEFAULTS=config['CACHE_CONTROL'],
        SECRET_KEY=os.urandom(24),
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
    )
    return settings
