import os

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


DEBUG = os.environ.get('DEBUG', False)
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SITE_URL = os.environ.get('SITE_URL', 'localhost')

USER_APP_NAME = 'Life Bartenders'
USER_ENABLE_EMAIL = True
USER_ENABLE_USERNAME = True
USER_REQUIRE_RETYPE_PASSWORD = False
USER_EMAIL_SENDER_NAME = os.environ.get('USER_EMAIL_SENDER_NAME')
USER_EMAIL_SENDER_EMAIL = os.environ.get('USER_EMAIL_SENDER_EMAIL')

# Flask-Mail SMTP server settings
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
MAIL_DEBUG = False

# image upload
UPLOAD_FOLDER = os.path.join(basedir, 'static/img/event_photos')
UPLOAD_COVER_FOLDER = os.path.join(basedir, 'static/img/event_covers')
UPLOAD_DEST = 'img/event_photos'
UPLOAD_COVER_DEST = 'img/event_covers'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
