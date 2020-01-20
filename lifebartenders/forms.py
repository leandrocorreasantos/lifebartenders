from wtforms import (
    Form, DateTimeField, BooleanField, SelectField,
    StringField, TextField, SubmitField, validators
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from lifebartenders.models import State


class EventForm(Form):
    title = StringField(u'Título', validators=[validators.DataRequired()])
    description = TextField(u'Descrição')
    date = DateTimeField(u'Data', validators=[validators.DataRequired()])
    place = StringField(u'Local', validators=[validators.DataRequired()])
    visible = BooleanField(u'Visível', default="checked")
    state = QuerySelectField(
        u'Estado', get_label='name',
        query_factory=lambda: (State.query.all())
    )
    city = SelectField(u'Cidade', choices=[])
    salva = SubmitField(u'Enviar')
