from hmac import new
from apiflask import APIBlueprint
from app.models import *

from app.extensions import auth
from flask import current_app, flash, request
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError
from functools import wraps


bp = APIBlueprint('blueprint', __name__, tag="default")


from app.blueprints.movie import bp as bp_movie
bp.register_blueprint(bp_movie, url_prefix='/movie')

from app.blueprints.screening import bp as bp_screening
bp.register_blueprint(bp_screening, url_prefix='/screening')

from app.blueprints.seat import bp as bp_seat
bp.register_blueprint(bp_seat, url_prefix='/seat')

from app.blueprints.theater import bp as bp_theater
bp.register_blueprint(bp_theater, url_prefix='/theater')

from app.blueprints.ticket import bp as bp_ticket
bp.register_blueprint(bp_ticket, url_prefix='/ticket')

from app.blueprints.ticketcategory import bp as bp_ticketcategory
bp.register_blueprint(bp_ticketcategory, url_prefix='/ticketcategory')

from app.blueprints.order import bp as bp_order
bp.register_blueprint(bp_order, url_prefix='/order')

from app.blueprints.ticketorder import bp as bp_ticketorder
bp.register_blueprint(bp_ticketorder, url_prefix='/ticketorder')

from app.blueprints.role import bp as bp_role
bp.register_blueprint(bp_role, url_prefix='/role')

from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.userrole import bp as bp_userrole
bp.register_blueprint(bp_userrole, url_prefix='/userrole')