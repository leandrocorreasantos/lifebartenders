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
    page = int(request.args.get('page', 1))
    offset = int(request.args.get('offset', 10))
    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).paginate(page, offset).items
    return render_template(
        'admin/agenda.html',
        agendas=agendas
    )


@admin.route('/eventos')
@login_required
def eventos():
    return render_template('admin/eventos.html')
