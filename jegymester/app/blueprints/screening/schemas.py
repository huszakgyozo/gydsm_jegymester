from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.screening import Screening


class ScreeningListSchema(Schema):
    id = fields.Integer()
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.String()
    deleted = fields.Boolean()


class ScreeningRequestSchema(Schema):
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.String()

class ScreeningResponseSchema(Schema):
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.String()

class ScreeningUpdateSchema(Schema):
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.String()
    deleted = fields.Boolean()

class ScreeningDeleteSchema(Schema):
    id = fields.Integer()


class ScreeningToTheaterSchema(Schema):
    start_time = fields.String()
    theater = fields.Nested('TheaterToSeatSchema')