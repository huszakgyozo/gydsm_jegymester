from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.theater import Theater


class TheaterListSchema(Schema):
    id = fields.Integer()
    theatname = fields.String()


class TheaterRequestSchema(Schema):
    theatname = fields.String()


class TheaterResponseSchema(Schema):
    theatname = fields.String()


class TheaterToSeatSchema(Schema):
    theatname = fields.String()
    seats = fields.Nested('SeatResponseSchema', many=True)