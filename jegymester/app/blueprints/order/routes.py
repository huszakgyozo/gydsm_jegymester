from app.blueprints.order import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.order.schemas import *
from app.blueprints.order.service import OrderService


@bp.route('/')
def index():
    return 'Order Blueprint'


@bp.get('/list_all')
@bp.output(OrderListSchema(many=True))
def order_list_all():
    success, response = OrderService.order_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_active')
@bp.output(OrderListSchema(many=True))
def order_list_active():
    success, response = OrderService.order_list_active()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(OrderResponseSchema)
def order_get_item(id):
    success, response = OrderService.order_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(OrderUpdateSchema, location="json")
@bp.output(OrderResponseSchema)
def order_update(id, json_data):
    success, response = OrderService.order_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def order_delete(id):
    success, response = OrderService.order_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

