import os
import json

CONFIG_PATH = "config.json"


def get_project_settings():
    if not os.path.isfile(CONFIG_PATH):
        print('A file with the name "config.json" was not found in the root directory')
        exit(1)

    config = json.loads(open(CONFIG_PATH).read())
    settings = dict(
        MAIL_SERVER=config['MAIL_SERVER'],
        MAIL_PORT=config['MAIL_PORT'],
        MAIL_USERNAME=config['MAIL_USERNAME'],
        MAIL_PASSWORD=config['MAIL_PASSWORD'],
        MAIL_RECIPIENTS=config['MAIL_RECIPIENTS'],
        AUTH_PASSWORD=config['AUTH_PASSWORD'],
        DATABASE='data.db',
        SECRET_KEY=os.urandom(24),
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
    )
    return settings
