from apiflask import APIBlueprint
from app.models import *

bp = APIBlueprint('main', __name__, tag="default")


@bp.route('/')
def index():
    return 'This is The Main Blueprint'

# from app.blueprints.user import bp as bp_user
# bp.register_blueprint(bp_user, url_prefix='/user')