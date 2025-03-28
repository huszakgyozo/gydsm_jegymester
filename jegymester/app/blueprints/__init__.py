from apiflask import APIBlueprint
from app.models import *

bp = APIBlueprint('main', __name__, tag="default")


@bp.route('/')
def index():
    return 'This is The Main Blueprint'

# from app.blueprints.user import bp as bp_user
# bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.movie import bp as bp_movie
bp.register_blueprint(bp_movie, url_prefix='/movie')

from app.blueprints.screening import bp as bp_screening
bp.register_blueprint(bp_screening, url_prefix='/screening')

from app.blueprints.seat import bp as bp_seat
bp.register_blueprint(bp_seat, url_prefix='/seat')

from app.blueprints.theater import bp as bp_theater
bp.register_blueprint(bp_theater, url_prefix='/theater')