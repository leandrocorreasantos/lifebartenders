from wtforms import (
    Form, DateTimeField, BooleanField, SelectField,
    StringField, TextField, SubmitField, validators
)


class EventForm(Form):
    title = StringField(u'Título', validators=[validators.DataRequired()])
    description = TextField(u'Descrição')
    date = DateTimeField(u'Data', validators=[validators.DataRequired()])
    place = StringField(u'Local', validators=[validators.DataRequired()])
    visible = BooleanField(u'Visível', default="checked")
    state = SelectField(u'Estado', choices=[])
    city = SelectField(u'Cidade', choices=[])
    salva = SubmitField(u'Enviar')
