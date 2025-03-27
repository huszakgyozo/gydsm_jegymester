from app.blueprints.movie import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from jegymester.app.blueprints.movie.schemas import *
from jegymester.app.blueprints.movie.service import MovieService

@bp.route('/')
def index():
    return 'Movie Blueprint'

@bp.get('/list/')
@bp.output(MovieListSchema(many = True))
def movie_list_all():
    success, response = MovieService.movie_list_all()
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
@bp.input(MovieRequestSchema, location="json")
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
