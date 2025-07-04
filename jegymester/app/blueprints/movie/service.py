﻿from app.extensions import db
from app.blueprints.movie.schemas import *

from app.models.movie import Movie

from sqlalchemy import null, select, and_


class MovieService:
    @staticmethod
    def movie_list_all():
        movies = db.session.execute(select(Movie).filter(
            Movie.deleted.is_(0))).scalars()
        return True, MovieToScreeningSchema().dump(movies,many=True)

    @staticmethod
    def movie_list_active():
        screenings = db.session.execute(select(Movie).filter(
            Movie.deleted.is_(0))).scalars()
        return True, MovieListSchema().dump(screenings, many=True)

    @staticmethod
    def movie_get_item(id):
        movie = db.session.get(Movie, id)
        if not movie:
            return False, "A film nem található!"
        return True, MovieResponseSchema().dump(movie)

    @staticmethod
    def movie_add(request):
        try:
            movie = Movie(**request)
            db.session.add(movie)
            db.session.commit()

        except Exception as ex:
            return False, "movie_add() hiba!"+str(ex)
        return True, MovieResponseSchema().dump(movie)

    @staticmethod
    def movie_update(id, request):
        try:
            movie = db.session.get(Movie, id)
            if movie:
                # movie.title = request["title"]
                # movie.duration = int(request["duration"])
                # movie.genre = request["genre"]
                # movie.age_limit = int(request["age_limit"])
                movie.description = request["description"]
                #movie.deleted = int(request["deleted"])
                db.session.commit()

        except Exception as ex:
            return False, "movie_update() hiba!"+str(ex)
        return True, MovieResponseSchema().dump(movie)

    @staticmethod
    def movie_delete(id):
        try:
            movie = db.session.get(Movie, id)
            if not movie:
                return False, "A film nem található!"
            elif movie:
                movie.deleted = 1
                db.session.commit()
                return True, "Az adott film törölve."

        except Exception as ex:
            return False, "movie_delete() hiba!"+str(ex)
        return True, "OK"

    @staticmethod
    def movie_screenings(id):
        movie = db.session.get(Movie, id)
        if not movie:
            return False, "A film nem található!"
        return True, MovieToScreeningSchema().dump(movie)
    