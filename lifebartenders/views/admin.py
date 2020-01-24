from datetime import datetime
from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for,
    make_response
)
from flask_user import login_required
from lifebartenders import db
from lifebartenders.models import Event, City, State
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
    agenda = Event()
    form = EventForm(request.form, obj=agenda)
    if request.method == 'POST':
        form.populate_obj(agenda)
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
        'admin/agenda_add.html',
        form=form,
        title_action='Adicionar'
    )


@admin.route('/agenda/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_agenda(event_id):
    agenda = Event.query.filter(Event.id == event_id).first()
    form = EventForm(request.form, obj=agenda)
    if request.method == 'POST' and form.validate():
        form.populate_obj(agenda)
        try:
            db.session.add(agenda)
            db.session.commit()
        except Exception as e:
            print('except: {}'.format(e))
            db.session.rollback()
        return redirect(url_for('admin.agenda'))

    state = State.query.first_or_404(agenda.city.state_id)
    cities = [(c.id, c.name) for c in City.query.filter(
        State.id == City.state_id
    ).filter(State.id == agenda.city.state_id).all()]
    form.state.default = state.id
    form.city_id.choices = cities
    form.city_id.default = agenda.city.id
    form.visible.checked = 'checked' if agenda.visible is True else ''

    return render_template(
        'admin/agenda_edit.html',
        form=form,
        agenda=agenda
    )


@admin.route('/agenda/delete/<id>')
@login_required
def delete_agenda(id):
    pass


@admin.route('/eventos')
@login_required
def eventos():
    return render_template('admin/eventos.html')
