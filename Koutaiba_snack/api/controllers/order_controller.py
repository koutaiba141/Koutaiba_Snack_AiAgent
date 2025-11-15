
from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from api.services import order_service
from api.utils.responses import json_response, error_response
from api.models import schemas
from typing import Optional

router = APIRouter()

@router.post("/orders", summary="Create new order")
async def create_order(order_data: schemas.OrderCreate):
    try:
        order = await order_service.create_order(order_data)
        return json_response(data=jsonable_encoder(order), message="Order created successfully", status_code=201)
    except HTTPException as e:
        return error_response(message=e.detail, status_code=e.status_code)

@router.get("/orders", summary="List all orders")
async def get_orders(status: Optional[str] = Query(None)):
    orders = await order_service.get_all_orders(status)
    return json_response(data=jsonable_encoder(orders), message="Orders retrieved successfully")

@router.get("/orders/{order_id}", summary="Get order details")
async def get_order(order_id: int):
    order = await order_service.get_order_by_id(order_id)
    if not order:
        return error_response(message=f"Order with ID {order_id} not found", status_code=404)
    return json_response(data=jsonable_encoder(order), message="Order details retrieved successfully")

@router.get("/orders/status/{status}", summary="Get orders by status")
async def get_orders_by_status(status: str):
    orders = await order_service.get_orders_by_status(status)
    return json_response(data=jsonable_encoder(orders), message=f"Orders with status '{status}' retrieved successfully")

@router.get("/orders/customer/{customer_name}", summary="Get order history by customer")
async def get_orders_by_customer(customer_name: str):
    orders = await order_service.get_orders_by_customer(customer_name)
    return json_response(data=jsonable_encoder(orders), message=f"Order history for '{customer_name}' retrieved successfully")

@router.put("/orders/{order_id}/status", summary="Update order status")
async def update_order_status(order_id: int, status_update: schemas.OrderUpdateStatus):
    updated_order = await order_service.update_order_status(order_id, status_update.status)
    if not updated_order:
        return error_response(message=f"Order with ID {order_id} not found", status_code=404)
    return json_response(data=jsonable_encoder(updated_order), message="Order status updated successfully")
