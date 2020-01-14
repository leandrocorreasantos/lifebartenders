from datetime import datetime
from flask import Blueprint, render_template, request
from flask_user import login_required
from lifebartenders.models import Event


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    agendas = Event.query.filter(Event.date > datetime.now()).all()
    eventos = Event.query.filter(Event.date <= datetime.now()).all()
    return render_template(
        'admin/dashboard.html',
        agendas=agendas,
        eventos=eventos
    )


@admin.route('/agenda')
@login_required
def agenda():
    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).all()
    return render_template(
        'admin/agenda.html',
        agendas=agendas
    )


@admin.route('/agenda/add')
@login_required
def add_agenda():
    pass


@admin.route('/agenda/edit/<id>')
@login_required
def edit_agenda(id):
    pass


@admin.route('/agenda/delete/<id>')
@login_required
def delete_agenda(id):
    pass


@admin.route('/eventos')
@login_required
def eventos():
    return render_template('admin/eventos.html')
