from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField, BooleanField, SelectField, TextAreaField,
    StringField, SubmitField, HiddenField, FileField, validators
)
from lifebartenders.models import Event, EventPhoto, State, City


class EventForm(FlaskForm):
    class Meta:
        model = Event

    title = StringField('Título', validators=[validators.DataRequired()])
    description = TextAreaField('Descrição')
    date = DateTimeField('Data', format='%d/%m/%Y %H:%M')
    place = StringField('Local', validators=[validators.DataRequired()])
    visible = BooleanField('Visível', default=True)
    cover = FileField('Capa')
    state = SelectField(
        'Estado', choices=[(s.id, s.name) for s in State.query.all()],
        id='Event.states', coerce=int
    )
    city_id = SelectField(
        'Cidade', choices=[(c.id, c.name) for c in City.query.all()],
        id='Event.cities', coerce=int
    )
    submit = SubmitField('Enviar')


class EventUploadForm(FlaskForm):
    class Meta:
        model = EventPhoto

    event_id = HiddenField()
    image = FileField('Imagem')
    submit = SubmitField('Upload')


class ContatoForm(FlaskForm):

    nome = StringField('Nome', validators=[validators.DataRequired()])
    telefone = StringField('Telefone')
    email = StringField('E-mail', validators=[
        validators.DataRequired(), validators.Email()
    ])
    mensagem = TextAreaField('Mensagem')
    submit = SubmitField('Enviar Mensagem')
