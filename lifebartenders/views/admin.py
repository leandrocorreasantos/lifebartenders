import os
from datetime import datetime
from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for,
    make_response, flash
)
from werkzeug.utils import secure_filename
from flask_user import login_required
from lifebartenders import db
from lifebartenders.utils import valid_extension
from lifebartenders.config import (
    UPLOAD_COVER_FOLDER, UPLOAD_COVER_DEST,
    UPLOAD_FOLDER, UPLOAD_DEST, basedir
)
from lifebartenders.models import Event, EventPhoto, City, State
from lifebartenders.forms import EventForm, EventUploadForm
from lifebartenders.schemas import CitiesSchema


admin = Blueprint('admin', __name__, url_prefix='/admin')
OFFSET = int(os.environ.get('OFFSET_PAGINATOR', 20))


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
    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).paginate(1, 20, False).items
    eventos = Event.query.filter(
        Event.date <= datetime.now()
    ).paginate(1, 20, False).items
    return render_template(
        'admin/dashboard.html',
        agendas=agendas,
        eventos=eventos
    )


@admin.route('/agenda')
@login_required
def agenda():
    page = request.args.get('page', 1, type=int)

    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).paginate(page, OFFSET, False)
    return render_template(
        'admin/agenda.html',
        agendas=agendas
    )


@admin.route('/agenda/add', methods=['GET', 'POST'])
@login_required
def add_agenda():
    agenda = Event()
    form = EventForm(request.form, obj=agenda)
    if request.method == 'POST' and form.validate():
        form.populate_obj(agenda)
        try:
            db.session.add(agenda)
            db.session.commit()
        except Exception as e:
            print('except: {}'.format(e))
            db.session.rollback()

        if 'cover' in request.files:
            file = request.files['cover']
            if valid_extension(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(UPLOAD_COVER_FOLDER, filename))
                except Exception as e:
                    print('except upload: {}'.format(e))

                agenda.cover = '{}/{}'.format(UPLOAD_COVER_DEST, filename)
                try:
                    print('update file')
                    db.session.flush()
                    db.session.commit()
                except Exception as e:
                    print('cover except: {}'.format(e))
                    db.session.rollback()

        # create folder to upload images
        event_folder = os.path.join(UPLOAD_FOLDER, '{}'.format(agenda.id))
        os.makedirs(event_folder)

        flash('Evento cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.agenda'))

    return render_template(
        'admin/agenda_add.html',
        form=form,
        agenda=agenda
    )


@admin.route('/agenda/<int:event_id>/edit', methods=['GET', 'POST'])
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
            print('Erro update: {}'.format(e))
            flash('Erro ao atualizar dados', 'error')
            db.session.rollback()
            return redirect(url_for('admin.agenda'))

        if 'cover' in request.files:
            file = request.files['cover']
            if valid_extension(file.filename):
                cover_to_delete = os.path.join(basedir, 'static', agenda.cover)
                filename = secure_filename(file.filename)
                # salva nova capa na pasta
                try:
                    file.save(os.path.join(UPLOAD_COVER_FOLDER, filename))
                except Exception as e:
                    print('Erro upload capa: {}'.format(e))
                    flash('Erro no upload da capa', 'error')
                    return redirect(url_for('admin.agenda'))

                # apaga capa antiga
                if os.path.isfile(cover_to_delete):
                    os.unlink(cover_to_delete)

                # salva nova capa no banco
                agenda.cover = '{}/{}'.format(UPLOAD_COVER_DEST, filename)
                try:
                    print('update file')
                    db.session.flush()
                    db.session.commit()
                except Exception as e:
                    print('erro ao salvar capa: {}'.format(e))
                    flash('Erro ao salvar capa no banco de dados', 'error')
                    db.session.rollback()
                    return redirect(url_for('admin.agenda'))

        flash('Evento {} editado com sucesso!'.format(event_id), 'success')
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


@admin.route('/agenda/delete', methods=['DELETE'])
@login_required
def delete_agenda():
    event_id = request.form.get('event_id')
    agenda = Event.query.get(event_id)
    try:
        db.session.delete(agenda)
        db.session.commit()
    except Exception as e:
        print('Error while delete agenda: {}'.format(e))
        flash('Erro ao excluir evento', 'error')
        db.session.rollback()

    cover_to_delete = os.path.join(basedir, 'static', agenda.cover)
    if os.path.isfile(cover_to_delete):
        os.unlink(cover_to_delete)

    return jsonify({}), 200


@admin.route('/eventos')
@login_required
def eventos():
    page = request.args.get('page', 1, type=int)

    eventos = Event.query.filter(
        Event.date <= datetime.now()
    ).paginate(page, OFFSET, False)

    return render_template(
        'admin/evento.html',
        eventos=eventos
    )


@admin.route('/eventos/<int:event_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_evento(event_id):
    evento = Event.query.get(event_id)
    photo = EventPhoto()
    form = EventUploadForm(request.form, obj=photo)
    if request.method == 'POST' and form.validate():
        event_folder = os.path.join(UPLOAD_FOLDER, '{}'.format(event_id))
        if 'image' in request.files:
            file = request.files['image']
            if valid_extension(file.filename):
                filename = secure_filename(file.filename)
                try:
                    filedest = '{}/{}/{}'.format(
                        UPLOAD_DEST, event_id, filename
                    )
                    file.save(os.path.join(event_folder, filename))
                except Exception as e:
                    print('except upload: {}'.format(e))

                photo.image = filedest
                photo.event_id = event_id
                try:
                    db.session.add(photo)
                    db.session.commit()
                except Exception as e:
                    print('Except save: {}'.format(e))
                    db.session.rollback()

    photos = EventPhoto.query.filter(EventPhoto.event_id == event_id).all()
    return render_template(
        'admin/evento_upload.html',
        evento=evento,
        form=form,
        photos=photos
    )


@admin.route('/eventos/photo/delete', methods=['DELETE'])
@login_required
def delete_photo():
    photo_id = request.form.get('id')
    photo = EventPhoto.query.get(photo_id)
    image_to_delete = os.path.join(basedir, 'static', photo.image)
    try:
        db.session.delete(photo)
        db.session.commit()
    except Exception as e:
        print('Error while delete image: {}'.format(e))
        db.session.rollback()
        return jsonify({}, 204)

    if os.path.isfile(image_to_delete):
        os.unlink(image_to_delete)

    return jsonify({}), 200
