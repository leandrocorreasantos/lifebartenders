from flask import Blueprint, render_template


site = Blueprint('site', __name__)


@site.route('/')
def index():
    return render_template('index.html')


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
