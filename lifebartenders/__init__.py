import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from lifebartenders.views.site import site
from lifebartenders.views.admin import admin


dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy()
db.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(site)
app.register_blueprint(admin)
