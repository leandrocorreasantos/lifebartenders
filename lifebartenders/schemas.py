from marshmallow import Schema, fields
from datetime import datetime


class StatesSchema(Schema):
    __tablename__ = 'states'

    id = fields.Integer()
    name = fields.String()
    fs = fields.String()


class CitiesSchema(Schema):
    __tablename__ = 'cities'

    id = fields.Integer()
    name = fields.String()
    state = fields.Nested('StatesSchema')
