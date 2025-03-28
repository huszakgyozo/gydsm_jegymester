from app.blueprints.theater import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.theater.schemas import *

from app.blueprints.theater.service import TheaterService


@bp.route('/')
def index():
    return 'Theater Blueprint'


@bp.get('/list/')
@bp.output(TheaterListSchema(many=True))
def theater_list_all():
    success, response = TheaterService.theater_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(TheaterResponseSchema)
def theater_get_item(id):
    success, response = TheaterService.theater_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(TheaterRequestSchema, location="json")
@bp.output(TheaterResponseSchema)
def theater_add_new(json_data):
    success, response = TheaterService.theater_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(TheaterRequestSchema, location="json")
@bp.output(TheaterResponseSchema)
def theater_update(id, json_data):
    success, response = TheaterService.theater_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def theater_delete(id):
    success, response = TheaterService.theater_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
