import os
import html
from datetime import datetime
from flask import (
    redirect,
    render_template,
    request,
    flash,
    make_response,
    url_for,
    jsonify
)
from werkzeug.utils import secure_filename
from lifebartenders import app, db
from lifebartenders.models import (
    Event,
    EventPhoto,
    State,
    City
)
from lifebartenders.schemas import (
    StatesSchema,
    CitiesSchema
)
from flask_user import login_required
from sqlalchemy import distinct
from sqlalchemy.sql.expression import extract
from lifebartenders import mail, log
from lifebartenders.config import (
    UPLOAD_COVER_FOLDER, UPLOAD_COVER_DEST,
    UPLOAD_FOLDER, UPLOAD_DEST, basedir, SITE_URL
)
from lifebartenders.utils import valid_extension
from lifebartenders.forms import ContatoForm, EventForm, EventUploadForm
from flask_mail import Message


@app.route('/')
@app.route('/home')
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


@app.route('/quem-somos')
def quem_somos():
    return render_template('quem_somos.html')


@app.route('/agenda')
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


@app.route('/eventos')
def eventos():
    eventos = Event.query.filter(
        Event.date < datetime.now()
    ).limit(16).all()

    return render_template(
        'eventos.html',
        eventos=eventos
    )


@app.route('/evento/<int:evento_id>/<evento_slug>')
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


@app.route('/contato', methods=['GET', 'POST'])
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


@app.route('/sitemap-<int:year>.xml')
def sitemap_by_year(year):
    eventos = Event.query.filter(
        Event.date < datetime.now()
    ).filter(
        extract('year', Event.date) == year
    ).order_by(
        Event.date
    ).all()

    sitemap_xml = render_template(
        'sitemap_by_year.xml',
        eventos=eventos,
        site=SITE_URL
    )

    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/sitemaps.xml')
def sitemaps():
    years = Event.query.with_entities(
        distinct(extract('year', Event.date))
    ).all()

    sitemap_xml = render_template(
        'sitemap_list.xml',
        years=years,
        site=SITE_URL
    )
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/sitemap.xml')
def static_sitemap():
    sitemap = render_template('sitemap_static.xml', site=SITE_URL)
    response = make_response(sitemap)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# admin views

OFFSET = int(os.environ.get('OFFSET_PAGINATOR', 20))


@app.route('/admin/_get_states')
@login_required
def get_states():
    states = []
    response = {}
    states = State.query.all()
    response = make_response(
        jsonify(StatesSchema(many=True, only=('id', 'name')).dump(states))
    )
    response.content_type = 'application/json'
    return response


@app.route('/admin/_get_cities/<state_id>')
@login_required
def get_cities(state_id):
    cities = []
    response = {}
    cities = City.query.filter(City.state_id == state_id).all()
    response = make_response(
        jsonify(CitiesSchema(many=True, only=('id', 'name')).dump(cities))
    )
    response.content_type = 'application/json'
    return response


@app.route('/admin')
@app.route('/admin/dashboard')
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


@app.route('/admin/agenda')
@login_required
def admin_agenda():
    page = request.args.get('page', 1, type=int)

    agendas = Event.query.filter(
        Event.date > datetime.now()
    ).paginate(page, OFFSET, False)
    return render_template(
        'admin/agenda.html',
        agendas=agendas
    )


@app.route('/admin/agenda/add', methods=['GET', 'POST'])
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
            log.error('except: {}'.format(e))
            db.session.rollback()

        if 'cover' in request.files:
            file = request.files['cover']
            if valid_extension(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(UPLOAD_COVER_FOLDER, filename))
                except Exception as e:
                    log.error('except upload: {}'.format(e))

                agenda.cover = '{}/{}'.format(UPLOAD_COVER_DEST, filename)
                try:
                    log.info('update file')
                    db.session.flush()
                    db.session.commit()
                except Exception as e:
                    log.error('cover except: {}'.format(e))
                    db.session.rollback()

        # create folder to upload images
        event_folder = os.path.join(UPLOAD_FOLDER, '{}'.format(agenda.id))
        os.makedirs(event_folder)

        flash('Evento cadastrado com sucesso!', 'success')
        return redirect(url_for('admin_agenda'))

    return render_template(
        'admin/agenda_add.html',
        form=form,
        agenda=agenda
    )


@app.route('/admin/agenda/<int:event_id>/edit', methods=['GET', 'POST'])
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
            log.error('Erro update: {}'.format(e))
            flash('Erro ao atualizar dados', 'error')
            db.session.rollback()
            return redirect(url_for('admin_agenda'))

        if 'cover' in request.files:
            cover_to_delete = ''
            file = request.files['cover']
            if valid_extension(file.filename):
                if agenda.cover:
                    cover_to_delete = os.path.join(
                        basedir, 'static', agenda.cover
                    )
                filename = secure_filename(file.filename)
                # salva nova capa na pasta
                try:
                    file.save(os.path.join(UPLOAD_COVER_FOLDER, filename))
                except Exception as e:
                    log.error('Erro upload capa: {}'.format(e))
                    flash('Erro no upload da capa', 'error')
                    return redirect(url_for('admin_agenda'))

                # apaga capa antiga
                if os.path.isfile(cover_to_delete):
                    os.unlink(cover_to_delete)

                # salva nova capa no banco
                agenda.cover = '{}/{}'.format(UPLOAD_COVER_DEST, filename)
                try:
                    log.info('update file')
                    db.session.flush()
                    db.session.commit()
                except Exception as e:
                    log.error('erro ao salvar capa: {}'.format(e))
                    flash('Erro ao salvar capa no banco de dados', 'error')
                    db.session.rollback()
                    return redirect(url_for('admin_agenda'))

        flash('Evento {} editado com sucesso!'.format(event_id), 'success')
        return redirect(url_for('admin_agenda'))

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


@app.route('/admin/agenda/delete', methods=['DELETE'])
@login_required
def delete_agenda():
    event_id = request.form.get('event_id')
    agenda = Event.query.get(event_id)
    try:
        db.session.delete(agenda)
        db.session.commit()
    except Exception as e:
        log.error('Error while delete agenda: {}'.format(e))
        flash('Erro ao excluir evento', 'error')
        db.session.rollback()

    cover_to_delete = os.path.join(basedir, 'static', agenda.cover)
    if os.path.isfile(cover_to_delete):
        os.unlink(cover_to_delete)

    return jsonify({}), 200


@app.route('/admin/eventos')
@login_required
def admin_eventos():
    page = request.args.get('page', 1, type=int)

    eventos = Event.query.filter(
        Event.date <= datetime.now()
    ).paginate(page, OFFSET, False)

    return render_template(
        'admin/evento.html',
        eventos=eventos
    )


@app.route('/admin/eventos/<int:event_id>/upload', methods=['GET', 'POST'])
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
                    log.error('except upload: {}'.format(e))

                photo.image = filedest
                photo.event_id = event_id
                try:
                    db.session.add(photo)
                    db.session.commit()
                except Exception as e:
                    log.error('Except save: {}'.format(e))
                    db.session.rollback()

    photos = EventPhoto.query.filter(EventPhoto.event_id == event_id).all()
    return render_template(
        'admin/evento_upload.html',
        evento=evento,
        form=form,
        photos=photos
    )


@app.route('/admin/eventos/photo/delete', methods=['DELETE'])
@login_required
def delete_photo():
    photo_id = request.form.get('id')
    photo = EventPhoto.query.get(photo_id)
    image_to_delete = os.path.join(basedir, 'static', photo.image)
    try:
        db.session.delete(photo)
        db.session.commit()
    except Exception as e:
        log.error('Error while delete image: {}'.format(e))
        db.session.rollback()
        return jsonify({}, 204)

    if os.path.isfile(image_to_delete):
        os.unlink(image_to_delete)

    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=app.debug, threaded=True, host='0.0.0.0', port=5000)
