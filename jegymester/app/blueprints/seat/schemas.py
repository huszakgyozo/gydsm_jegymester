from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.seat import Seat


class SeatListSchema(Schema):
    id = fields.Integer()
    theater_id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()


class SeatRequestSchema(Schema):
    theater_id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()


class SeatResponseSchema(Schema):
    seat_number = fields.String()
    reserved = fields.Boolean()


class SeatDeleteSchema(Schema):
    id = fields.Integer()


class SeatUpdateSchema(Schema):
    theater_id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()