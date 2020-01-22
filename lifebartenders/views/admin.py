from datetime import datetime
from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for,
    make_response
)
from flask_user import login_required
from lifebartenders import db
from lifebartenders.models import Event, City
from lifebartenders.forms import EventForm
from lifebartenders.schemas import CitiesSchema


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/_get_cities/<state_id>')
def get_cities(state_id):
    cities = []
    response = {}
    cities = City.query.filter(City.state_id == state_id).all()
    response = make_response(
        jsonify(CitiesSchema(many=True, only=('id', 'name')).dump(cities))
    )
    response.content_type = 'application/json'
    return response


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


@admin.route('/agenda/add', methods=['GET', 'POST'])
@login_required
def add_agenda():
    form = EventForm(request.form)
    print(form.data)
    if request.method == 'POST':
        agenda = Event()
        form.populate_obj(agenda)
        print(agenda.__dict__)
        if form.validate():
            try:
                db.session.add(agenda)
                db.session.commit()
            except Exception as e:
                print('except: {}'.format(e))
                db.session.rollback()
            return redirect(url_for('admin.agenda'))
        else:
            print(form.errors)

    return render_template(
        'admin/agenda_form.html',
        form=form,
        title_action='Adicionar'
    )


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
