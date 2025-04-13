from app.blueprints.seat import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.seat.schemas import *
from app.blueprints.seat.service import SeatService
from app.extensions import auth
from app.blueprints import role_required

@bp.route('/')
def index():
    return 'Seat Blueprint'


@bp.get('/list/')
@bp.output(SeatListSchema(many=True))
@bp.auth_required(auth)
@role_required([1])
def seat_list_all():
    success, response = SeatService.seat_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(SeatResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def seat_get_item(id):
    success, response = SeatService.seat_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def seat_update(id, json_data):
    success, response = SeatService.seat_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
