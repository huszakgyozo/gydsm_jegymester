from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.models.movie import Movie


class MovieListSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()
    deleted = fields.Boolean()


class MovieRequestSchema(Schema):
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()


class MovieResponseSchema(Schema):
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()

class MovieUpdateSchema(Schema):
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()
    deleted = fields.Boolean()


class MovieDeleteSchema(Schema):
    id = fields.Integer()


class MovieToScreeningSchema(Schema):
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()
    screenings = fields.Nested('ScreeningToTheaterSchema', many=True)

class ScreeningMovieSchema(Schema):
    title = fields.String()