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

USER_APP_NAME = 'lifebartenders'
USER_ENABLE_EMAIL = True
USER_ENABLE_USERNAME = True
USER_REQUIRE_RETYPE_PASSWORD = False

# Flask-Mail SMTP server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
MAIL_DEBUG = False
