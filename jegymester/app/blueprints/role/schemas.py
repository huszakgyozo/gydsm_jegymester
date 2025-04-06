from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.role import Role

#ma
class RoleListSchema(Schema):
    id = fields.Integer()
    role_name=fields.String()
    deleted=fields.Bool()

class RoleRequestSchema(Schema):
    role_name=fields.String()
    deleted=fields.Bool()

class RoleResponseSchema(Schema):
    role_name=fields.String()
    deleted=fields.Bool()

class RoleUpdateSchema(Schema):
    role_name=fields.String()
    deleted=fields.Bool()

class RoleDeleteSchema(Schema):
    id = fields.String()

