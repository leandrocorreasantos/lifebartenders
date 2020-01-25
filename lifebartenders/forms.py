from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField, BooleanField, SelectField, TextAreaField,
    StringField, SubmitField, validators
)
from lifebartenders.models import Event, State, City


class EventForm(FlaskForm):
    class Meta:
        model = Event

    title = StringField('Título', validators=[validators.DataRequired()])
    description = TextAreaField('Descrição')
    date = DateTimeField('Data', format='%d/%m/%Y %H:%M')
    place = StringField('Local', validators=[validators.DataRequired()])
    visible = BooleanField('Visível', default=True)
    state = SelectField(
        'Estado', choices=[(s.id, s.name) for s in State.query.all()],
        id='Event.states', coerce=int
    )
    city_id = SelectField(
        'Cidade', choices=[(c.id, c.name) for c in City.query.all()],
        id='Event.cities', coerce=int
    )
    submit = SubmitField('Enviar')
