from apiflask import APIBlueprint

bp = APIBlueprint('ticketorder', __name__, tag="ticketorder")

from app.blueprints.ticketorder import routes