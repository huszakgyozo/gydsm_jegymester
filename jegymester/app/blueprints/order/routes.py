﻿from app.blueprints.order import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.order.schemas import *
from app.blueprints.order.service import OrderService
from app.extensions import auth
from app.routes.auth import role_required

@bp.route('/')
def index():
    return 'Order Blueprint'


@bp.get('/list_all')
@bp.output(OrderListSchema(many=True))
@bp.auth_required(auth)
@role_required([1,2,3])
def order_list_all():
    success, response = OrderService.order_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(OrderResponseSchema)
@bp.auth_required(auth)
@role_required([1,3])
def order_get_item(id):
    success, response = OrderService.order_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(OrderUpdateSchema, location="json")
@bp.output(OrderResponseSchema)
@bp.auth_required(auth)
@role_required([1,3])
def order_update(id, json_data):
    success, response = OrderService.order_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
@bp.auth_required(auth)
@role_required([1,2,3])
def order_delete(id):
    success, response = OrderService.order_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

