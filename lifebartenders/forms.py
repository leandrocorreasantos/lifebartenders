from wtforms import (
    DateTimeField, BooleanField, SelectField, TextAreaField,
    StringField, SubmitField, HiddenField, FileField, PasswordField,
    validators
)
from lifebartenders.models import Event, EventPhoto
try:
    from flask_wtf import FlaskForm
except ImportError:
    from flask_wtf import Form as FlaskForm


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
        'Estado', choices=[],
        id='Event.states', coerce=int
    )
    city_id = SelectField(
        'Cidade', choices=[],
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


class LoginForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[validators.DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[validators.DataRequired()]
    )
    submit = SubmitField('Login')
