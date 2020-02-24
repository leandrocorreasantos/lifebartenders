from flask import Blueprint, render_template, request, flash
from lifebartenders.models import Event, EventPhoto
from datetime import datetime
from lifebartenders.forms import ContatoForm
from lifebartenders import mail, log
from flask_mail import Message
import html


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

    return render_template(
        'agenda_view.html',
        evento=evento,
        fotos=fotos
    )


@site.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm(request.form)
    if request.method == 'POST':
        msg = Message(
            'Contato do site lifebartenders',
            sender=(form.nome.data, form.email.data),
            recipients=['leandro.admo@gmail.com'],
            reply_to=form.email.data
        )
        mensagem = 'Nome: {}\n E-mail: {}\n Telefone:{}\n Mensagem: {}'.format(
            form.nome.data,
            form.email.data,
            form.telefone.data,
            html.escape(form.mensagem.data)
        )
        msg.body = mensagem

        try:
            with mail.connect() as conn:
                conn.send(mensagem)
            flash('Mensagem enviada com sucesso!', 'success')
            log.info('mensagem enviada')
        except Exception as e:
            log.error('Erro ao enviar mensagem: {}'.format(e))
            flash('Desculpe, não foi posível enviar a mensagem', 'error')

    return render_template(
        'contato.html',
        form=form
    )
