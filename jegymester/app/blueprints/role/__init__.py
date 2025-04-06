from apiflask import APIBlueprint

bp = APIBlueprint('role', __name__, tag="role")

from app.blueprints.role import routes