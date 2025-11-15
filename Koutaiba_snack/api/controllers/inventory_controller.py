
from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from api.services import inventory_service
from api.utils.responses import json_response, error_response
from api.models import schemas

router = APIRouter()

@router.get("/ingredients", summary="List all ingredients with stock")
async def get_ingredients():
    ingredients = await inventory_service.get_all_ingredients()
    return json_response(data=jsonable_encoder(ingredients), message="Ingredients retrieved successfully")

@router.get("/ingredients/{ingredient_id}", summary="Get specific ingredient details")
async def get_ingredient(ingredient_id: int):
    ingredient = await inventory_service.get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return error_response(message=f"Ingredient with ID {ingredient_id} not found", status_code=404)
    return json_response(data=jsonable_encoder(ingredient), message="Ingredient details retrieved successfully")

@router.get("/ingredients/items/{item_id}", summary="Get ingredients for a menu item")
async def get_ingredients_for_item(item_id: int):
    ingredients = await inventory_service.get_ingredients_for_item(item_id)
    if not ingredients:
        return error_response(message=f"No ingredients found for item with ID {item_id}", status_code=404)
    return json_response(data=jsonable_encoder(ingredients), message="Ingredients for item retrieved successfully")

@router.get("/ingredients/low-stock", summary="Show low-stock ingredients")
async def get_low_stock_ingredients():
    ingredients = await inventory_service.get_low_stock_ingredients()
    return json_response(data=jsonable_encoder(ingredients), message="Low-stock ingredients retrieved successfully")

@router.get("/stock/check-item/{item_id}", summary="Check if item can be made")
async def check_item_availability(item_id: int, quantity: int = Query(1, gt=0)):
    can_be_made = await inventory_service.check_item_availability(item_id, quantity)
    return json_response(data={"can_be_made": can_be_made}, message=f"Stock availability check for item {item_id}")

@router.put("/ingredients/{ingredient_id}/stock", summary="Update stock level")
async def update_stock(ingredient_id: int, stock_update: schemas.StockUpdate):
    updated_ingredient = await inventory_service.update_stock_level(ingredient_id, stock_update.quantity)
    if not updated_ingredient:
        return error_response(message=f"Ingredient with ID {ingredient_id} not found", status_code=404)
    return json_response(data=jsonable_encoder(updated_ingredient), message="Stock level updated successfully")
