from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.ticketorder import TicketOrder


class TicketOrderListSchema(Schema):
    order_id = fields.Integer()
    ticket_id = fields.Integer()
    ticket_active = fields.Bool()


class TicketOrderRequestSchema(Schema):
    ticket_active = fields.Bool()
    order_id = fields.Integer()
    ticket_id = fields.Integer()


class TicketOrderResponseSchema(Schema):
    ticket_active = fields.Bool()
    order_id = fields.Integer()
    ticket_id = fields.Integer()


class TicketOrderToTicket(Schema):
    ticket_active = fields.Bool()