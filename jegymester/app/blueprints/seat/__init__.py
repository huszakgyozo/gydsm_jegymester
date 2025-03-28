from apiflask import APIBlueprint

bp = APIBlueprint('seat', __name__, tag="seat")

from app.blueprints.seat import routes