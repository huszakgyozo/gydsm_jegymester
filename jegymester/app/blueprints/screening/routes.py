from app.blueprints.screening import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from jegymester.app.blueprints.screening.schemas import *
from jegymester.app.blueprints.screening.service import ScreeningService

@bp.route('/')
def index():
    return 'Screening Blueprint'

@bp.get('/list/')
@bp.output(ScreeningListSchema(many = True))
def screening_list_all():
    success, response = ScreeningService.screening_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(ScreeningResponseSchema)
def screening_get_item(id):
    success, response = ScreeningService.screening_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/add/')
@bp.input(ScreeningRequestSchema, location="json")
@bp.output(ScreeningResponseSchema)
def screening_add_new(json_data):
    success, response = ScreeningService.screening_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/update/<int:id>')
@bp.input(ScreeningRequestSchema, location="json")
@bp.output(ScreeningResponseSchema)
def screening_update(id, json_data):
    success, response = ScreeningService.screening_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.delete('/delete/<int:id>')
def screening_delete(id):
    success, response = ScreeningService.screening_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)