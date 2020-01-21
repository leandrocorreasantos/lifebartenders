from marshmallow import Schema, fields


class States(Schema):
    __tablename__ = 'states'

    id = fields.Integer()
    name = fields.String()
    fs = fields.String()


class Cities(Schema):
    __tablename__ = 'cities'

    id = fields.Integer()
    name = fields.String()
    state = fields.Nested('States')
