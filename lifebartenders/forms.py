from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField, BooleanField,
    StringField, TextField, SubmitField, validators
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from lifebartenders.models import State, Event, City


class EventForm(FlaskForm):
    class Meta:
        model = Event

    title = StringField('Título', validators=[validators.DataRequired()])
    description = TextField('Descrição')
    date = DateTimeField('Data', validators=[validators.DataRequired()])
    place = StringField('Local', validators=[validators.DataRequired()])
    visible = BooleanField('Visível', default="checked")
    state = QuerySelectField(
        u'Estado', get_label='name',
        query_factory=lambda: (State.query.all()),
        id='Event.states'
    )
    # city_id = SelectField(
    #     'Cidade', choices=[],
    #     id='Event.cities', coerce=int
    # )
    city = QuerySelectField(
        'Cidade', id='Event.cities',
        query_factory=lambda: (City.query.all()),
        get_label=lambda a: str(a.name),
        get_pk=lambda a: a.id
    )
    submit = SubmitField('Enviar')
