from app.blueprints.seat import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.seat.schemas import *
from app.blueprints.seat.service import SeatService


@bp.route('/')
def index():
    return 'Seat Blueprint'


@bp.get('/list/')
@bp.output(SeatListSchema(many=True))
def seat_list_all():
    success, response = SeatService.seat_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(SeatResponseSchema)
def seat_get_item(id):
    success, response = SeatService.seat_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
def seat_add_new(json_data):
    success, response = SeatService.seat_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
def seat_update(id, json_data):
    success, response = SeatService.seat_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def seat_delete(id):
    success, response = SeatService.seat_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)