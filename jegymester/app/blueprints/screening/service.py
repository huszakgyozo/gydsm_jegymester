from app.extensions import db
from jegymester.app.blueprints.screening.schemas import *

from app.models.screening import Screening

from sqlalchemy import null, select, and_

class ScreeningService:
    @staticmethod
    def screening_list_all():
        screenings = db.session.execute(select(Screening)).scalars().all()
        return True, ScreeningListSchema().dump(screenings, many=True)

    @staticmethod
    def screening_get_item(id):
        screening = db.session.get(Screening, id)
        if not screening:
            return False, "A vetítés nem található!"
        return True, ScreeningResponseSchema().dump(screening)

    @staticmethod
    def screening_add(request):
        try:
            screening = Screening(**request)
            db.session.add(screening)
            db.session.commit()

        except Exception as ex:
            return False, "screening_add() hiba!"
        return True, ScreeningResponseSchema().dump(screening)

    @staticmethod
    def screening_update(id, request):
        try:
            screening = db.session.get(Screening, id)
            if screening:
                screening.movie_id = request["movie_id"]
                screening.theater_id = request["theater_id"]
                screening.start_time = request["start_time"]
                db.session.commit()

        except Exception as ex:
            return False, "screening_update() hiba!"
        return True, ScreeningResponseSchema().dump(screening)

    @staticmethod
    def screening_delete(id):
        try:
            screening = db.session.get(Screening, id)
            if not screening:
                return False, "A vetítés nem található!"
            elif screening:
                db.session.delete(screening)
                db.session.commit()
                return True, "Az adott vetítés törölve."

        except Exception as ex:
            return False, "screening_delete() hiba!"
        return True, "OK"