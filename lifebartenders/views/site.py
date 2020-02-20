from flask import Blueprint, render_template
from lifebartenders.models import Event
from datetime import datetime


site = Blueprint('site', __name__)


@site.route('/')
@site.route('/home')
def index():
    next_event = Event.query.filter(
        Event.date > datetime.now()
    ).order_by(
        Event.date
    ).first()

    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).limit(16).all()

    eventos = Event.query.filter(
        Event.date < datetime.now()
    ).limit(16).all()

    return render_template(
        'index.html',
        next_event=next_event,
        agendas=agendas,
        eventos=eventos
    )


@site.route('/quem-somos')
def quem_somos():
    return render_template('quem_somos.html')


@site.route('/agenda')
def agenda():
    return render_template('agenda.html')


@site.route('/agenda/<int:evento_id>/<evento_slug>')
def agenda_view(evento_id, evento_slug):
    return render_template('agenda_view.html')


@site.route('/eventos')
def eventos():
    return render_template('eventos.html')


@site.route('/contato')
def contato():
    return render_template('contato.html')
