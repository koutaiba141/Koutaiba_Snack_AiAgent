
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from api.services import customer_service
from api.utils.responses import json_response

router = APIRouter()

@router.get("/customers", summary="List customers from past orders")
async def get_customers():
    customers = await customer_service.get_all_customers()
    return json_response(data=jsonable_encoder(customers), message="Customers retrieved successfully")

@router.get("/analytics/popular-items", summary="Most ordered items")
async def get_popular_items():
    items = await customer_service.get_popular_items()
    return json_response(data=jsonable_encoder(items), message="Popular items retrieved successfully")

@router.get("/analytics/revenue", summary="Revenue statistics")
async def get_revenue_stats():
    stats = await customer_service.get_revenue_stats()
    return json_response(data=jsonable_encoder(stats), message="Revenue statistics retrieved successfully")
