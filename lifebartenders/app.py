from flask import render_template
from lifebartenders import app, db
from lifebartenders.views.site import site
from lifebartenders.views.admin import admin
from lifebartenders.models import User
from flask_user import UserManager

user_manager = UserManager(app, db, User)

app.register_blueprint(site)
app.register_blueprint(admin)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=app.debug, threaded=True, host='0.0.0.0', port=5000)
