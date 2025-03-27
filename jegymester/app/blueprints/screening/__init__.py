from apiflask import APIBlueprint

bp = APIBlueprint('screening', __name__, tag="screening")

from app.blueprints.screening import routes