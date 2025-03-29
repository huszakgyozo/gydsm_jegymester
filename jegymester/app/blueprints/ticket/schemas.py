from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.ticket import Ticket


class TicketListSchema(Schema):
    id = fields.Integer()
    screening_id = fields.Integer()
    user_id=fields.Integer()
    ticketcategory_id=fields.Integer()
    

class TicketRequestSchema(Schema):
    screening_id = fields.Integer()
    user_id=fields.Integer() 
    ticketcategory_id=fields.Integer()
    


class TicketResponseSchema(Schema):
    screening_id = fields.Integer()
    ticketcategory_id=fields.Integer()
    

class TicketToSeatSchema(Schema):
    screening_id = fields.Integer() 
    ticketcategory_id=fields.Integer()
    seats = fields.Nested('SeatResponseSchema', many=True)


    #javítandó
class TicketToTicketOrder(Schema):
    ticket_id = fields.Integer()
    ticket_orders = fields.Nested('TicketOrderToTicket')
    # userből ticket, ticketből ticketorder, ticketorderből order ?
