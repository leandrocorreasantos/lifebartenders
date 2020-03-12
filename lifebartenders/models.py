from lifebartenders import app, db
from flask_user import UserMixin, UserManager
from datetime import datetime


class BaseModel:
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.Boolean, default=False)


user_manager = UserManager(app, db, User)


class State(db.Model, BaseModel):
    __tablename__ = 'states'

    name = db.Column(db.String(100), nullable=False)
    fs = db.Column(db.String(2), nullable=False)


class City(db.Model, BaseModel):
    __tablename__ = 'cities'

    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey(
        'states.id',
        onupdate='CASCADE',
        ondelete='RESTRICT'
    ))
    state = db.relationship('State', backref='city')


class Event(db.Model, BaseModel):
    __tablename__ = 'events'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    date = db.Column(db.DateTime(), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    visible = db.Column(db.Boolean(), default=True)
    cover = db.Column(db.String(255))
    city_id = db.Column(db.Integer(), db.ForeignKey(
        'cities.id',
        onupdate='CASCADE',
        ondelete='RESTRICT'
    ))
    city = db.relationship('City', backref='event')
    photos = db.relationship('EventPhoto', backref='event')

    @property
    def slug(self):
        return '{}-{}-{}'.format(
            self.title.lower().replace(' ', '-'),
            self.city.name.lower().replace(' ', '-'),
            self.date.strftime('%d-%m-%Y')
        )

    @classmethod
    def next_event(cls):
        return cls.query.filter(
            Event.date > datetime.now()
        ).order_by(
            Event.date
        ).first()


class EventPhoto(db.Model, BaseModel):
    __tablename__ = 'events_photos'

    image = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer(), db.ForeignKey(
        'events.id',
        onupdate='CASCADE',
        ondelete='RESTRICT'
    ))
    # event = db.relationship('Event', backref='event_photo')
