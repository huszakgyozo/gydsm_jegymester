from apiflask import APIBlueprint

bp = APIBlueprint('movie', __name__, tag="movie")

from app.blueprints.movie import routes