from app.extensions import db
from app.blueprints.ticketorder.schemas import *

from app.models.ticketorder import TicketOrder

from sqlalchemy import null, select, and_


class TicketOrderService:
    @staticmethod
    def ticketorder_list_all():
        ticketorders = db.session.execute(select(TicketOrder)).scalars().all()
        return True, TicketOrderListSchema().dump(ticketorders, many=True)

    @staticmethod
    def ticketorder_delete(id):
        try:
            ticketorder = db.session.get(TicketOrder, id)
            if not ticketorder:
                return False, "A rendelés nem található!"
            elif ticketorder:
                ticketorder.ticket_active = 0
                db.session.commit()
                return True, "Az adott rendelés törölve."

        except Exception as ex:
            return False, "ticketorder_delete() hiba!"+str(ex)
        return True, "OK"