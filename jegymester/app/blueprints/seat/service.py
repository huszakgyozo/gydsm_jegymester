from app.extensions import db
from app.blueprints.seat.schemas import *

from app.models.seat import Seat

from sqlalchemy import null, select, and_


class SeatService:
    @staticmethod
    def seat_list_all():
        seats = db.session.execute(select(Seat)).scalars().all()
        return True, SeatListSchema().dump(seats, many=True)

    @staticmethod
    def seat_get_item(id):
        seat = db.session.get(Seat, id)
        if not seat:
            return False, "A szék nem található!"
        return True, SeatResponseSchema().dump(seat)

    @staticmethod
    def seat_add(request):
        try:
            seat = Seat(**request)
            db.session.add(seat)
            db.session.commit()

        except Exception as ex:
            return False, "seat_add() hiba!"
        return True, SeatResponseSchema().dump(seat)

    @staticmethod
    def seat_update(id, request):
        try:
            seat = db.session.get(Seat, id)
            if seat:
                seat.theater_id = request["theater_id"]
                seat.seat_number = request["seat_number"]
                seat.reserved = request["reserved"]
                db.session.commit()
        except Exception as ex:
            return False, "seat_update() hiba!"
        return True, SeatResponseSchema().dump(seat)

    @staticmethod
    def seat_delete(id):
        try:
            seat = db.session.get(Seat, id)
            if not seat:
                return False, "A szék nem található!"
            elif seat:
                db.session.delete(seat)
                db.session.commit()
                return True, "Az adott szék törölve."
        except Exception as ex:
            return False, "seat_delete() hiba!"
        return True, "OK"

