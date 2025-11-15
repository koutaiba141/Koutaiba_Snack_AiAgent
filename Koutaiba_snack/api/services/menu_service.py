
from api.database.supabase_conn import supabase
from api.models import schemas
from typing import List, Dict

async def get_full_menu() -> Dict[str, List[schemas.Item]]:
    response = supabase.from_("items").select("*, categories(name)").order("name").execute()
    menu = {}
    for item in response.data:
        category_name = "Uncategorized"
        if item.get('categories') and item['categories'].get('name'):
            category_name = item['categories']['name']
        
        if category_name not in menu:
            menu[category_name] = []
        menu[category_name].append(schemas.Item(**item))
    return menu

async def get_all_categories() -> List[schemas.Category]:
    response = supabase.from_("categories").select("*").order("name").execute()
    return [schemas.Category(**row) for row in response.data]

async def get_items_by_category_name(category_name: str) -> List[schemas.Item]:
    response = supabase.from_("categories").select("items(*)").eq("name", category_name).order("name").execute()
    if not response.data:
        return []
    return [schemas.Item(**item) for item in response.data[0]['items']]

async def get_item_by_id(item_id: int) -> schemas.Item:
    response = supabase.from_("items").select("*").eq("id", item_id).execute()
    if response.data:
        return schemas.Item(**response.data[0])
    return None

async def search_menu_items(query: str) -> List[schemas.Item]:
    response = supabase.from_("items").select("*").ilike("name", f"%{query}%").order("name").execute()
    return [schemas.Item(**row) for row in response.data]

async def get_available_items() -> List[schemas.Item]:
    response = supabase.from_("items").select("*").eq("available", True).order("name").execute()
    return [schemas.Item(**row) for row in response.data]
