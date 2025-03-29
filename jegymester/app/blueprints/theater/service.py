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

