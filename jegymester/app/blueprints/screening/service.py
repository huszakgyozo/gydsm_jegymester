﻿from app.extensions import db
from app.blueprints.screening.schemas import *

from app.models.screening import Screening

from sqlalchemy import null, select, and_
from datetime import datetime

class ScreeningService:
    @staticmethod
    def screening_list_all():
        screenings = db.session.execute(select(Screening)).scalars()
        return True, ScreeningListSchema().dump(screenings, many=True)

    @staticmethod
    def screening_list_active():
        screenings = db.session.execute(select(Screening).filter(
            Screening.deleted.is_(0))).scalars()
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
            return False, "screening_add() hiba!"+str(ex)
        return True, ScreeningResponseSchema().dump(screening)

    @staticmethod
    def screening_update(id, request):
        try:
            screening = db.session.get(Screening, id)
            if screening:
                screening.movie_id = request["movie_id"]
                screening.theater_id = request["theater_id"]
                screening.start_time = datetime.strptime(request["start_time"], "%Y-%m-%d %H:%M:%S")
                screening.deleted = request["deleted"]
                db.session.commit()

        except Exception as ex:
            return False, f"screening_update() hiba!{str(ex)}"
        return True, ScreeningResponseSchema().dump(screening)

    @staticmethod
    def screening_delete(id):
        try:
            screening = db.session.get(Screening, id)
            if not screening:
                return False, "A vetítés nem található!"
            elif screening:
                screening.deleted = 1
                db.session.commit()
                return True, "Az adott vetítés törölve."

        except Exception as ex:
            return False, "screening_delete() hiba!"+str(ex)
        return True, "OK"