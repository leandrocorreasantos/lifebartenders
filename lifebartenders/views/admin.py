from flask import Blueprint, render_template


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/agenda')
def agenda():
    return render_template('admin/agenda.html')

@admin.route('/eventos')
def eventos():
    return render_template('admin/eventos.html')
