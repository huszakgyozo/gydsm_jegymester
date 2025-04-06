from apiflask import APIBlueprint

bp = APIBlueprint('userrole', __name__, tag="userrole")

from app.blueprints.userrole import routes