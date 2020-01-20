from wtforms import (
    Form, DateTimeField, BooleanField,
    StringField, TextField, SubmitField, validators
)


class EventForm(Form):
    title = StringField(u'Título', validators=[validators.DataRequired()])
    description = TextField(u'Descrição')
    date = DateTimeField(u'Data', validators=[validators.DataRequired()])
    place = StringField(u'Local', validators=[validators.DataRequired()])
    visible = BooleanField(u'Visível')
    state = StringField(u'Estado')
    city = StringField(u'Cidade')
    salva = SubmitField(u'Enviar')
