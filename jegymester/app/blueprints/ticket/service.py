from app.extensions import db
from app.blueprints.ticket.schemas import *

from app.models.ticket import Ticket
from app.models.seat import Seat

from sqlalchemy import null, select, and_


class TicketService:
    @staticmethod
    def ticket_list_all():
        tickets = db.session.execute(select(Ticket)).scalars().all()
        return True, TicketListSchema().dump(tickets, many=True)

    def ticket_reserved_list_all():
        tickets = db.session.execute(select(Ticket).filter(
        Ticket.seat.has(Seat.reserved == True))).scalars().all()
        return True, TicketListSchema().dump(tickets, many=True)


    @staticmethod
    def ticket_get_item(id):
        ticket = db.session.get(Ticket, id)
        if not ticket:
            return False, "A jegy nem található!"
        return True, TicketResponseSchema().dump(ticket)

    @staticmethod
    def ticket_add(request):
        try:
            ticket = Ticket(**request)
            db.session.add(ticket)
            db.session.commit()

        except Exception as ex:
            return False, "ticket_add() hiba!"+str(ex)
        return True, TicketResponseSchema().dump(ticket)

    @staticmethod
    def ticket_update(id, request):
        try:
            ticket = db.session.get(Ticket, id)
            if ticket:
                ticket.ticketcategory_id = request["ticketcategory_id"]
                ticket.user_id = request["user_id "]
                ticket.screening_id = request["screening_id"]
                db.session.commit()

        except Exception as ex:
            return False, "ticket_update() hiba!"+str(ex)
        return True, TicketResponseSchema().dump(ticket)
    
    @staticmethod
    def get_ticket(id):
        ticket = db.session.get(Ticket, id)
        if not ticket:
            return False, "get_ticket() hiba!"
        return True, TicketToTicketOrder().dump(ticket)
