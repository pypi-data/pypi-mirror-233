import logging
from os import environ, urandom

from flask import Flask
from flask.cli import load_dotenv
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from transmission_rpc.client import Client

load_dotenv()

IS_DEBUG = environ.get('FLASK_ENV', 'production') == 'development'
ADMIN_USERNAME = environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD', 'secret')
APP_PORT = int(environ.get('FLASK_PORT', 5000))
CACHE_TIMEOUT = int(environ.get('CACHE_TIMEOUT', 60 * 60))
REQUESTS_TIMEOUT = int(environ.get('REQUESTS_TIMEOUT', 5))
BLACKLIST_WORDS = environ.get('BLACKLIST_WORDS', '').split(',') if environ.get('BLACKLIST_WORDS', '') else []
DB_ENABLED = False
REDIS_ENABLED = False
TRANSMISSION_ENABLED = False

app = Flask(__name__)
app.name = 'PyNyaaTa'
app.debug = IS_DEBUG
app.secret_key = urandom(24).hex()
app.url_map.strict_slashes = False
auth = HTTPBasicAuth()
logging.basicConfig(level=(logging.DEBUG if IS_DEBUG else logging.INFO))
logger = logging.getLogger(app.name)

db_uri = environ.get('DATABASE_URI')
if db_uri:
    DB_ENABLED = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = IS_DEBUG
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 200
    }
    db = SQLAlchemy(app)
    from .models import create_all

    create_all()

cache_host = environ.get('REDIS_SERVER')
if cache_host:
    REDIS_ENABLED = True
    cache = Redis(cache_host)

transmission_host = environ.get('TRANSMISSION_SERVER')
if transmission_host:
    TRANSMISSION_ENABLED = True
    transmission_username = environ.get('TRANSMISSION_RPC_USERNAME')
    transmission_password = environ.get('TRANSMISSION_RPC_PASSWORD')
    transmission = Client(
        username=transmission_username,
        password=transmission_password,
        host=transmission_host,
        logger=logger
    )
