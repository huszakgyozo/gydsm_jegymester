from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email, Length
from app.models.userrole import UserRole

#ma

class UserroleListSchema(Schema):
    id = fields.Integer()
    role_id = fields.Integer()

class UserroleRequestSchema(Schema):
    id = fields.Integer()
    role_id = fields.Integer()

class UserroleResponseSchema(Schema):
    id = fields.Integer()
    role_id = fields.Integer()

class UserroleUpdateSchema(Schema):
    id = fields.Integer()
    role_id = fields.Integer()
    deleted = fields.Boolean()

class UserroleDeleteSchema(Schema):
    id = fields.Integer()