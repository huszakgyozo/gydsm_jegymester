from app.extensions import db
from app.blueprints.ticketcategory.schemas import *

from app.models.ticketcategory import TicketCategory

from sqlalchemy import null, select, and_


class TicketCategoryService:
    @staticmethod
    def ticketcategory_list_all():
        ticketcategory = db.session.execute(select(TicketCategory)).scalars().all()
        return True, TicketCategoryListSchema().dump(ticketcategory, many=True)

    @staticmethod
    def ticketcategory_get_item(id):
        ticketcategory = db.session.get(TicketCategory, id)
        if not ticketcategory:
            return False, "A jegykategória nem található!"
        return True, TicketCategoryResponseSchema().dump(ticketcategory)


    @staticmethod
    def ticketcategory_update(id, request):
        try:
            ticketcategory = db.session.get(TicketCategory, id)
            if ticketcategory:
                ticketcategory.catname= request["catname"]
                ticketcategory.price=request["price"]
                db.session.commit()

        except Exception as ex:
            return False, "ticketcategory_update() hiba!"
        return True, TicketCategoryResponseSchema().dump(ticketcategory)
