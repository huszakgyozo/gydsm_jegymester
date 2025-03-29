from apiflask import APIBlueprint

bp = APIBlueprint('ticketcategory', __name__, tag="ticketcategory")

from app.blueprints.ticketcategory import routes