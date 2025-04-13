from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.role import Role

#ma
class RoleListSchema(Schema):
    id = fields.Integer()
    rolename=fields.String()

class RoleRequestSchema(Schema):
    rolename=fields.String()

class RoleResponseSchema(Schema):
    rolename=fields.String()

class RoleUpdateSchema(Schema):
    rolename=fields.String()

class RoleDeleteSchema(Schema):
    id = fields.String()

