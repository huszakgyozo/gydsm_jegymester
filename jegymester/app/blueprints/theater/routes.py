from app.blueprints.theater import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.theater.schemas import *
from app.blueprints.theater.service import TheaterService
from app.extensions import auth
from app.routes.auth import role_required

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


