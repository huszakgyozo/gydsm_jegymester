from app.extensions import db
from app.blueprints.theater.schemas import *

from app.models.theater import Theater

from sqlalchemy import null, select, and_


class TheaterService:
    @staticmethod
    def theater_list_all():
        theaters = db.session.execute(select(Theater)).scalars().all()
        return True, TheaterListSchema().dump(theaters, many=True)

    @staticmethod
    def theater_get_item(id):
        theater = db.session.get(Theater, id)
        if not theater:
            return False, "A terem nem található!"
        return True, TheaterResponseSchema().dump(theater)

    @staticmethod
    def theater_add(request):
        try:
            theater = Theater(**request)
            db.session.add(theater)
            db.session.commit()
        except Exception as ex:
            return False, "theater_add() hiba!"
        return True, TheaterResponseSchema().dump(theater)

    @staticmethod
    def theater_update(id, request):
        try:
            theater = db.session.get(Theater, id)
            if theater:
                theater.theatname = request["theatname"]
                db.session.commit()

        except Exception as ex:
            return False, "theater_update() hiba!"
        return True, TheaterResponseSchema().dump(theater)

    @staticmethod
    def theater_delete(id):
        try:
            theater = db.session.get(Theater, id)
            if not theater:
                return False, "A terem nem található!"
            elif theater:
                db.session.delete(theater)
                db.session.commit()
                return True, "Az adott terem törölve."

        except Exception as ex:
            return False, f"theater_delete() hiba!{ex}"
        return True, "OK"