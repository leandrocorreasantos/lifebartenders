from flask import Blueprint, render_template, request
from lifebartenders.models import Event, EventPhoto
from datetime import datetime


site = Blueprint('site', __name__)


@site.route('/')
@site.route('/home')
def index():
    next_event = Event.next_event()

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
    next_event = Event.next_event()
    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).order_by(
        Event.date
    ).limit(12).all()
    return render_template(
        'agenda.html',
        agendas=agendas,
        next_event=next_event
    )


@site.route('/eventos')
def eventos():
    eventos = Event.query.filter(
        Event.date < datetime.now()
    ).limit(16).all()

    return render_template(
        'eventos.html',
        eventos=eventos
    )


@site.route('/evento/<int:evento_id>/<evento_slug>')
def agenda_view(evento_id, evento_slug):
    page = request.args.get('page', 1, type=int)
    offset = request.args.get('offset', 8, type=int)
    evento = Event.query.get(evento_id)
    fotos = EventPhoto.query.filter(
        Event.id == EventPhoto.event_id
    ).paginate(page, offset, False)

    print(fotos.__dict__)

    return render_template(
        'agenda_view.html',
        evento=evento,
        fotos=fotos
    )


@site.route('/contato')
def contato():
    return render_template('contato.html')
