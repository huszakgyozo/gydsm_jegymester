from dataclasses import field
from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email, Length
from app.models.userrole import UserRole

# ma


class UserroleListSchema(Schema):
    role_id = fields.Integer()
    user_id = fields.Integer()


class UserroleRequestSchema(Schema):
    role_id = fields.Integer()
    user_id = fields.Integer()


class UserroleResponseSchema(Schema):
    role_id = fields.Integer()
    user_id = fields.Integer()


class UserroleUpdateSchema(Schema):
    newrole_id = fields.Integer()