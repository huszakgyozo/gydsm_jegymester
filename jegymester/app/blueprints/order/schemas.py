from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.order import Order


class OrderListSchema(Schema):
    id = fields.Integer()
    payment_status=fields.String()
    deleted=fields.Bool()

class OrderRequestSchema(Schema):
    payment_status=fields.String()
    deleted=fields.Bool()

class OrderResponseSchema(Schema):
    payment_status=fields.String()
    deleted=fields.Bool()

class OrderUpdateSchema(Schema):
    payment_status=fields.String()
    deleted=fields.Bool()

class OrderDeleteSchema(Schema):
    id = fields.String()

