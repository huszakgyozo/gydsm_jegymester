from apiflask import APIBlueprint

bp = APIBlueprint('ticket', __name__, tag="ticket")

from app.blueprints.ticket import routes