import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.config.from_object('lifebartenders.config')

db = SQLAlchemy(app)

mail = Mail(app)
