
from api.database.supabase_conn import supabase
from api.models import schemas
from typing import List
from fastapi import HTTPException

async def create_order(order_data: schemas.OrderCreate) -> schemas.Order:
    # 1. Check stock for all items in the order
    print("Checking stock...")
    for item in order_data.items:
        response = supabase.from_("item_ingredients").select("quantity_required, ingredients(name, current_stock)").eq("item_id", item.item_id).execute()
        print(f"Stock check response for item {item.item_id}: {response}")
        if not response.data:
            raise HTTPException(status_code=400, detail=f"Item with ID {item.item_id} has no ingredients.")

        for row in response.data:
            if row['ingredients']['current_stock'] < row['quantity_required'] * item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for item: {row['ingredients']['name']}")

    # 2. Create the order and get the order ID
    print("Creating order...")
    order_response = supabase.from_("orders").insert({
        "customer_name": order_data.customer_name,
        "customer_phone": order_data.customer_phone,
        "table_number": order_data.table_number,
        "notes": order_data.notes
    }).execute()
    print(f"Create order response: {order_response}")

    if not order_response.data:
        raise HTTPException(status_code=500, detail="Could not create order.")

    order_id = order_response.data[0]['id']

    # 3. Insert order items and update stock
    print("Inserting order items and updating stock...")
    total_amount = 0
    for item in order_data.items:
        # Get item price
        item_price_response = supabase.from_("items").select("price").eq("id", item.item_id).execute()
        print(f"Item price response for item {item.item_id}: {item_price_response}")
        unit_price = item_price_response.data[0]['price']
        total_amount += unit_price * item.quantity

        # Insert order item
        order_item_response = supabase.from_("order_items").insert({
            "order_id": order_id,
            "item_id": item.item_id,
            "quantity": item.quantity,
            "unit_price": unit_price,
            "notes": item.notes
        }).execute()
        print(f"Insert order item response for item {item.item_id}: {order_item_response}")

        # Update ingredient stock
        item_ingredients_response = supabase.from_("item_ingredients").select("ingredient_id, quantity_required").eq("item_id", item.item_id).execute()
        print(f"Item ingredients response for item {item.item_id}: {item_ingredients_response}")
        for ingredient in item_ingredients_response.data:
            ingredient_id = ingredient['ingredient_id']
            quantity_required = ingredient['quantity_required']

            # Get current stock
            ingredient_stock_response = supabase.from_("ingredients").select("current_stock").eq("id", ingredient_id).execute()
            print(f"Ingredient stock response for ingredient {ingredient_id}: {ingredient_stock_response}")
            current_stock = ingredient_stock_response.data[0]['current_stock']

            # Update stock
            update_stock_response = supabase.from_("ingredients").update({"current_stock": current_stock - (quantity_required * item.quantity)}).eq("id", ingredient_id).execute()
            print(f"Update stock response for ingredient {ingredient_id}: {update_stock_response}")

    # 4. Update the total amount for the order
    print("Updating total amount...")
    update_total_response = supabase.from_("orders").update({"total_amount": total_amount}).eq("id", order_id).execute()
    print(f"Update total amount response: {update_total_response}")

    # 5. Fetch and return the created order
    print("Fetching created order...")
    created_order_response = supabase.from_("orders").select("*").eq("id", order_id).execute()
    print(f"Created order response: {created_order_response}")
    return schemas.Order(**created_order_response.data[0])

async def get_all_orders(status: str = None) -> List[schemas.Order]:
    print("Getting all orders...")
    query = supabase.from_("orders").select("*").order("created_at", desc=True)
    if status:
        query = query.eq("status", status)
    response = query.execute()
    print(f"Get all orders response: {response}")
    return [schemas.Order(**row) for row in response.data]

async def get_order_by_id(order_id: int) -> schemas.Order:
    order_response = supabase.from_("orders").select("*, order_items(*)").eq("id", order_id).single().execute()
    if not order_response.data:
        return None

    order_data = order_response.data
    order_items_raw = order_data.pop('order_items', [])

    order_items_parsed = [schemas.OrderItem(**item) for item in order_items_raw]

    order_data['items'] = order_items_parsed
    return schemas.Order(**order_data)

async def get_orders_by_status(status: str) -> List[schemas.Order]:
    response = supabase.from_("orders").select("*").eq("status", status).order("created_at", desc=True).execute()
    return [schemas.Order(**row) for row in response.data]

async def get_orders_by_customer(customer_name: str) -> List[schemas.Order]:
    response = supabase.from_("orders").select("*").ilike("customer_name", f"%{customer_name}%").order("created_at", desc=True).execute()
    return [schemas.Order(**row) for row in response.data]

async def update_order_status(order_id: int, status: str) -> schemas.Order:
    from datetime import datetime
    response = supabase.from_("orders").update({"status": status, "updated_at": datetime.now().isoformat()}).eq("id", order_id).execute()
    if response.data:
        return schemas.Order(**response.data[0])
    return None
