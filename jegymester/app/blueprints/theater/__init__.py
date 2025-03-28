from apiflask import APIBlueprint

bp = APIBlueprint('theater', __name__, tag="theater")

from app.blueprints.theater import routes