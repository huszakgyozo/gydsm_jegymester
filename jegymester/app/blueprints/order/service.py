from app.extensions import db
from app.blueprints.order.schemas import *

from app.models.order import Order, StatusEnum
from sqlalchemy import delete, null, select, and_

class OrderService:
    @staticmethod
    def order_list_all():
        orders = db.session.execute(select(Order)).scalars()
        return True, OrderListSchema().dump(orders, many=True)

    @staticmethod
    def order_get_item(id):
        order = db.session.get(Order, id)
        if not order:
            return False, "A megrendelés nem található!"
        return True, OrderResponseSchema().dump(order)

    @staticmethod
    def order_add(request):
        try:
            order = Order(**request)
            db.session.add(order)
            db.session.commit()

        except Exception as ex:
            return False, "order_add() hiba!"+str(ex)
        return True, OrderResponseSchema().dump(order)

    @staticmethod
    def order_update(id, request):
        try:
            order = db.session.get(Order, id)
            if order:
                payment_status = request.get("payment_status")

                # Validáljuk és konvertáljuk a payment_status értéket
                order.payment_status = StatusEnum.validate(payment_status)

                order.deleted = request.get("deleted")

                db.session.commit()
                return True, order
            else:
                return False, "Nincs ilyen order"
        except Exception as ex:
            return False, "order_update() hiba!"+str(ex)
        return True, OrderResponseSchema().dump(order)
            
    @staticmethod
    def order_delete(id):
        try:
            order = db.session.get(Order, id)
            if not order:
                return False, "A megrendelés nem található!"
            elif order:
                order.deleted=1
                db.session.commit()
                return True, "Az adott megrendelés törölve."

        except Exception as ex:
            return False, "order_delete() hiba!"+str(ex)
        return True, "OK"
    
