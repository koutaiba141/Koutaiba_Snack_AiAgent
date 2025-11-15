"""
Restaurant API Tools for LangChain Agent
"""
import requests
import json
from typing import Optional, Dict, Any
from langchain.tools import Tool
from pydantic import BaseModel, Field

BASE_URL = "http://127.0.0.1:8000"

# Pydantic models for structured inputs
class OrderItem(BaseModel):
    """Model for order item"""
    item_id: int = Field(description="The ID of the menu item")
    quantity: int = Field(description="Quantity of the item")
    notes: Optional[str] = Field(default="", description="Special notes for this item")

class CreateOrderInput(BaseModel):
    """Input for creating an order"""
    customer_name: str = Field(description="Customer's full name")
    customer_phone: str = Field(description="Customer's phone number")
    table_number: Optional[int] = Field(default=None, description="Table number if dining in")
    notes: Optional[str] = Field(default="", description="General order notes")
    items_json: str = Field(description="JSON string of items list with item_id, quantity, and notes")

class SearchMenuInput(BaseModel):
    """Input for searching menu"""
    query: str = Field(description="Search query for menu items")

class CategoryInput(BaseModel):
    """Input for category search"""
    category: str = Field(description="Category name to filter items")

class ItemIdInput(BaseModel):
    """Input for item ID operations"""
    item_id: int = Field(description="The menu item ID")

class CheckStockInput(BaseModel):
    """Input for checking stock"""
    item_id: int = Field(description="The menu item ID")
    quantity: int = Field(description="Quantity to check")

class CustomerNameInput(BaseModel):
    """Input for customer search"""
    customer_name: str = Field(description="Customer's name to search orders")

# API Functions
def get_complete_menu(input_data=None) -> str:
    """Get the complete restaurant menu with all items and details.no additional positional arguments needed"""
    try:
        response = requests.get(f"{BASE_URL}/menu")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching menu: {str(e)}"

def list_categories(input_data=None) -> str:
    """List all available food categories in the menu. nopositional arguments is needed """
    try:
        response = requests.get(f"{BASE_URL}/menu/categories")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching categories: {str(e)}"

def get_items_by_category(category: str) -> str:
    """Get all menu items in a specific category."""
    try:
        response = requests.get(f"{BASE_URL}/menu/categories/{category}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching items for category {category}: {str(e)}"

def get_item_details(item_id: int) -> str:
    """Get detailed information about a specific menu item by its ID."""
    try:
        response = requests.get(f"{BASE_URL}/menu/items/{item_id}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching item details for ID {item_id}: {str(e)}"

def search_menu(query: str) -> str:
    """Search for menu items by name or description."""
    try:
        response = requests.get(f"{BASE_URL}/menu/search", params={"q": query})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error searching menu with query '{query}': {str(e)}"

def get_available_items(input_data = None) -> str:
    """Get only the menu items that are currently available."""
    try:
        response = requests.get(f"{BASE_URL}/menu/available")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching available items: {str(e)}"

def check_item_stock(item_id: int, quantity: int) -> str:
    """Check if a menu item can be made in the requested quantity."""
    try:
        response = requests.get(f"{BASE_URL}/stock/check-item/{item_id}", params={"quantity": quantity})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error checking stock for item {item_id}: {str(e)}"

def check_item_stock_wrapper(data: Dict[str, Any]) -> str:
    """Wrapper for check_item_stock to be used in a Tool."""
    return check_item_stock(item_id=data['item_id'], quantity=data['quantity'])

def get_item_ingredients(item_id: int) -> str:
    """Get the list of ingredients for a specific menu item."""
    try:
        response = requests.get(f"{BASE_URL}/ingredients/items/{item_id}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching ingredients for item {item_id}: {str(e)}"

def create_order(customer_name: str, customer_phone: str, items_json: str,
                table_number: Optional[int] = None, notes: str = "") -> str:
    """
    Create a new order for a customer.

    Args:
        customer_name: Customer's full name
        customer_phone: Customer's phone number
        items_json: JSON string of items, e.g. '[{"item_id": 1, "quantity": 2, "notes": "Extra cheese"}]'
        table_number: Optional table number for dine-in
        notes: Optional general order notes
    """
    try:
        # Parse items from JSON string
        items = json.loads(items_json)

        order_data = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "table_number": table_number,
            "notes": notes,
            "items": items
        }

        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except json.JSONDecodeError:
        return f"Error: Invalid items JSON format. Expected format: '[{{\"item_id\": 1, \"quantity\": 2}}]'"
    except Exception as e:
        return f"Error creating order: {str(e)}"

def create_order_wrapper(data: Dict[str, Any]) -> str:
    """Wrapper for create_order to be used in a Tool."""
    return create_order(
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        items_json=data['items_json'],
        table_number=data.get('table_number'),
        notes=data.get('notes', '')
    )

def get_customer_orders(customer_name: str) -> str:
    """Get order history for a specific customer by their name."""
    try:
        response = requests.get(f"{BASE_URL}/orders/customer/{customer_name}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching orders for customer {customer_name}: {str(e)}"

# Create LangChain Tools
tools = [
    Tool(
        name="get_complete_menu",
        func=get_complete_menu,
        description="Use this to get the complete restaurant menu with all items, prices, and details. Use when customer asks 'what do you have' or wants to see everything available."
    ),
    Tool(
        name="list_categories",
        func=list_categories,
        description="Use this to list all food categories available (e.g., Pizza, Burgers, Drinks). Use when customer asks about types of food available."
    ),
    Tool(
        name="get_items_by_category",
        func=get_items_by_category,
        description="Use this to get all items in a specific category. Input should be the category name (e.g., 'Pizza', 'Burgers'). Use when customer asks about specific type of food.",
        args_schema=CategoryInput
    ),
    Tool(
        name="get_item_details",
        func=get_item_details,
        description="Use this to get detailed information about a specific menu item including price, description, and availability. Input should be the item ID number.",
        args_schema=ItemIdInput
    ),
    Tool(
        name="search_menu",
        func=search_menu,
        description="Use this to search for menu items by name or keywords. Input should be the search term (e.g., 'cheese', 'spicy'). Use when customer mentions specific ingredients or flavors.",
        args_schema=SearchMenuInput
    ),
    Tool(
        name="get_available_items",
        func=get_available_items,
        description="Use this to get only items that are currently available and in stock. Use when customer wants to know what can be ordered right now."
    ),
    Tool(
        name="check_item_stock",
        func=check_item_stock_wrapper,
        description="Use this to check if an item can be made in the requested quantity before placing order. Input format: item_id (int), quantity (int). Always check stock before creating an order.",
        args_schema=CheckStockInput
    ),
    Tool(
        name="get_item_ingredients",
        func=get_item_ingredients,
        description="Use this to get the list of ingredients for a menu item. Input should be the item ID. Use when customer asks about ingredients or has allergies.",
        args_schema=ItemIdInput
    ),
    Tool(
        name="create_order",
        func=create_order_wrapper,
        description="""Use this to create a new order. Required inputs:
        - customer_name: Full name (str)
        - customer_phone: Phone number (str) 
        - items_json: JSON string of items in format '[{"item_id": 1, "quantity": 2, "notes": "optional"}]'
        Optional:
        - table_number: Table number if dining in (int)
        - notes: General order notes (str)
        
        IMPORTANT: Before creating order, make sure you have collected ALL required information from customer:
        1. Customer name
        2. Phone number
        3. Items with quantities
        4. Ask if dining in (table number) or takeaway
        
        Always check stock availability before creating the order!""",
        args_schema=CreateOrderInput
    ),
    Tool(
        name="get_customer_orders",
        func=get_customer_orders,
        description="Use this to get past order history for a customer. Input should be the customer's name. Use when customer asks about their previous orders.",
        args_schema=CustomerNameInput
    )
]