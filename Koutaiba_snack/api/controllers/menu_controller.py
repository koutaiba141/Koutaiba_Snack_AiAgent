
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from api.services import menu_service
from api.utils.responses import json_response, error_response
from api.models import schemas

router = APIRouter()

@router.get("/menu", summary="Get complete menu")
async def get_menu():
    menu = await menu_service.get_full_menu()
    return json_response(data=jsonable_encoder(menu), message="Complete menu retrieved successfully")

@router.get("/menu/categories", summary="List all categories")
async def get_categories():
    categories = await menu_service.get_all_categories()
    return json_response(data=jsonable_encoder(categories), message="Categories retrieved successfully")

@router.get("/menu/categories/{category_name}", summary="Get items by category")
async def get_items_by_category(category_name: str):
    items = await menu_service.get_items_by_category_name(category_name)
    if not items:
        return error_response(message=f"No items found for category: {category_name}", status_code=404)
    return json_response(data=jsonable_encoder(items), message=f"Items for category '{category_name}' retrieved successfully")

@router.get("/menu/items/{item_id}", summary="Get specific item details")
async def get_item(item_id: int):
    item = await menu_service.get_item_by_id(item_id)
    if not item:
        return error_response(message=f"Item with ID {item_id} not found", status_code=404)
    return json_response(data=jsonable_encoder(item), message="Item details retrieved successfully")

@router.get("/menu/search", summary="Search menu items")
async def search_items(q: str):
    items = await menu_service.search_menu_items(q)
    return json_response(data=jsonable_encoder(items), message=f"Search results for '{q}'")

@router.get("/menu/available", summary="Get only available items")
async def get_available_items():
    items = await menu_service.get_available_items()
    return json_response(data=jsonable_encoder(items), message="Available items retrieved successfully")
