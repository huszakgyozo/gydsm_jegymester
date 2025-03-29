from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.ticketcategory import TicketCategory


class TicketCategoryListSchema(Schema):
    id = fields.Integer()
    catname = fields.String()
    price = fields.Integer()


class TicketCategoryRequestSchema(Schema):
   price = fields.Integer()
   catname = fields.String()


class TicketCategoryResponseSchema(Schema):
    catname = fields.String()
    price = fields.Integer()



class TicketCategoryUpdateSchema(Schema):
    price = fields.Integer()

