from marshmallow import Schema, fields, post_load

from .models import Person


class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer()
    address = fields.String()
    work = fields.String()

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)
