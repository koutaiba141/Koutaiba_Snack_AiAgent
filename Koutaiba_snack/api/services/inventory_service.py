
from api.database.supabase_conn import supabase
from api.models import schemas
from typing import List

async def get_all_ingredients() -> List[schemas.Ingredient]:
    response = supabase.from_("ingredients").select("*").order("name").execute()
    return [schemas.Ingredient(**row) for row in response.data]

async def get_ingredient_by_id(ingredient_id: int) -> schemas.Ingredient:
    response = supabase.from_("ingredients").select("*").eq("id", ingredient_id).execute()
    if response.data:
        return schemas.Ingredient(**response.data[0])
    return None

async def get_ingredients_for_item(item_id: int) -> List[dict]:
    response = supabase.from_("item_ingredients").select("quantity_required, ingredients(name, unit)").eq("item_id", item_id).execute()
    return [{"name": row['ingredients']['name'], "quantity_required": row['quantity_required'], "unit": row['ingredients']['unit']} for row in response.data]

async def get_low_stock_ingredients() -> List[schemas.Ingredient]:
    response = supabase.from_("ingredients").select("*").order("name").execute()
    low_stock_ingredients = [schemas.Ingredient(**row) for row in response.data if row['current_stock'] <= row['min_stock_level']]
    return low_stock_ingredients

async def check_item_availability(item_id: int, quantity: int) -> bool:
    response = supabase.from_("item_ingredients").select("quantity_required, ingredients(current_stock)").eq("item_id", item_id).execute()
    if not response.data:
        return False  # Item has no ingredients

    for row in response.data:
        if row['ingredients']['current_stock'] < row['quantity_required'] * quantity:
            return False
    return True

async def update_stock_level(ingredient_id: int, new_quantity: float) -> schemas.Ingredient:
    response = supabase.from_("ingredients").update({"current_stock": new_quantity}).eq("id", ingredient_id).execute()
    if response.data:
        return schemas.Ingredient(**response.data[0])
    return None
