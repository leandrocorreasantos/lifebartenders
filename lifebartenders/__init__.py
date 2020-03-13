import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_images import Images
from flask_user import UserManager
import logging
import logging.config
import sys


dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

db = SQLAlchemy()
mail = Mail()
images = Images()


def create_app():
    app = Flask(__name__)
    app.config.from_object('lifebartenders.config')
    db.init_app(app)
    mail.init_app(app)
    images.init_app(app)
    from lifebartenders.models import User
    user_manager = UserManager(app, db, User)  # noqa
    return app

app = create_app()

handler = logging.StreamHandler(sys.stdout)
if not app.config.get('DEBUG'):
    handler = logging.handlers.RotatingFileHandler(
        'app.log', maxBytes=102400, backupCount=3
    )

formater = logging.Formatter(
    '{"timestamp": "%(asctime)s", '
    '"level": "%(levelname)s", '
    '"module": "%(module)s", '
    '"function": "%(funcName)s", '
    '"file": "%(filename)s", '
    '"line": "%(lineno)d", '
    '"message": "%(message)s"}',
    "%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formater)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)
