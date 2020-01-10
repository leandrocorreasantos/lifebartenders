from datetime import datetime
from flask import Blueprint, render_template
from lifebartenders.models import Event


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin.route('/dashboard')
def dashboard():
    agendas = Event.query.filter(Event.date > datetime.now()).all()
    eventos = Event.query.filter(Event.date <= datetime.now()).all()
    return render_template(
        'admin/dashboard.html',
        agendas=agendas,
        eventos=eventos
    )


@admin.route('/agenda')
def agenda():
    return render_template('admin/agenda.html')


@admin.route('/eventos')
def eventos():
    return render_template('admin/eventos.html')
