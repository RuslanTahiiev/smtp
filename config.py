from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'cfg.env'))


class Config:
    # Config
    EMAIL = environ.get('EMAIL_EMAIL')
    PASSWORD = environ.get('EMAIL_PASSWORD')

