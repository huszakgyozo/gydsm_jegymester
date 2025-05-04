from dataclasses import field
from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email, Length
from app.models.user import User
from app import models

class UserRequestSchema(Schema):
    email = String(validate=Email(), required=True)
    password_hash = fields.String()
    phone = fields.String()

class UserResponseSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()
    token = fields.String()


class UserLoginSchema(Schema):
    email = String(validate=Email(), required=True)
    password_hash = fields.String(required=True)


class UserListSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()
    tickets = fields.Nested('TicketResponseSchema', many=True)


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class PayloadSchema(Schema):
    id = fields.Integer()
    email =fields.String()
    roles = fields.List(fields.Nested(RoleSchema))
    exp = fields.Integer()

class UserUpdateSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()