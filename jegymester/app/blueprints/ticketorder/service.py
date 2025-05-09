﻿from app.extensions import db
from app.blueprints.ticketorder.schemas import *

from app.models.ticketorder import TicketOrder

from sqlalchemy import null, select, and_

from app.models.seat import Seat
from app.models.ticket import Ticket


class TicketOrderService:
    @staticmethod
    def ticketorder_list_all():
        ticketorders = db.session.execute(select(TicketOrder)).scalars().all()
        return True, TicketOrderListSchema().dump(ticketorders, many=True)

    @staticmethod
    def ticketorder_delete(id):
        try:
            ticketorder = db.session.execute(select(TicketOrder).filter(
            TicketOrder.ticket_id==id)).first()

            if not ticketorder:
                return False, "A rendelés nem található!"
            elif ticketorder:
                ticketorder[0].ticket_active = 0

                tick=db.session.get(Ticket, id)
                db.session.flush()
                seat=db.session.get(Seat, tick.seat_id)
                seat.reserved = False
                db.session.commit()
                return True, "Az adott rendelés törölve."

        except Exception as ex:
            return False, "ticketorder_delete() hiba!"+str(ex)
        return True, "OK"