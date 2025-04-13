from app.blueprints.movie import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.movie.schemas import *
from app.blueprints.movie.service import MovieService
from app.extensions import auth
from app.blueprints import role_required

@bp.route('/')
def index():
    return 'Movie Blueprint'


@bp.get('/list_all')
@bp.output(MovieListSchema(many=True))
def movie_list_all():
    success, response = MovieService.movie_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_active')
@bp.output(MovieListSchema(many=True))
def movie_list_active():
    success, response = MovieService.movie_list_active()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(MovieResponseSchema)
def movie_get_item(id):
    success, response = MovieService.movie_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(MovieRequestSchema, location="json")
@bp.output(MovieResponseSchema)
def movie_add_new(json_data):
    success, response = MovieService.movie_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(MovieUpdateSchema, location="json")
@bp.output(MovieResponseSchema)
def movie_update(id, json_data):
    success, response = MovieService.movie_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def movie_delete(id):
    success, response = MovieService.movie_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/screenings/<int:id>')
@bp.output(MovieToScreeningSchema)
def movie_screenings(id):
    success, response = MovieService.movie_screenings(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)