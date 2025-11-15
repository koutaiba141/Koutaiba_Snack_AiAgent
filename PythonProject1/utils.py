"""
Utility functions for the Koutaiba Snack AI Agent
"""
import re
from typing import Dict, Any, Optional


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format

    Args:
        phone: Phone number string

    Returns:
        True if valid format, False otherwise
    """
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)

    # Check if it contains only digits and is reasonable length
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def format_phone_number(phone: str) -> str:
    """
    Format phone number to a standard format

    Args:
        phone: Raw phone number string

    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    return digits


def validate_order_data(order_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate order data before submission

    Args:
        order_data: Dictionary containing order information

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['customer_name', 'customer_phone', 'items']

    # Check required fields
    for field in required_fields:
        if field not in order_data or not order_data[field]:
            return False, f"Missing required field: {field}"

    # Validate customer name
    if len(order_data['customer_name'].strip()) < 2:
        return False, "Customer name must be at least 2 characters"

    # Validate phone number
    if not validate_phone_number(order_data['customer_phone']):
        return False, "Invalid phone number format"

    # Validate items list
    if not isinstance(order_data['items'], list) or len(order_data['items']) == 0:
        return False, "Order must contain at least one item"

    # Validate each item
    for item in order_data['items']:
        if 'item_id' not in item or 'quantity' not in item:
            return False, "Each item must have item_id and quantity"

        if not isinstance(item['quantity'], int) or item['quantity'] < 1:
            return False, "Item quantity must be a positive integer"

    return True, None


def parse_order_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract order information from natural language text
    This is a helper for parsing customer messages

    Args:
        text: Natural language text containing order info

    Returns:
        Dictionary with extracted order data or None
    """
    # This is a simple implementation - can be enhanced with NLP
    order_data = {}

    # Try to extract phone number
    phone_pattern = r'\b\d{7,15}\b'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        order_data['phone'] = phone_match.group()

    return order_data if order_data else None


def format_price(price: float) -> str:
    """
    Format price for display

    Args:
        price: Price as float

    Returns:
        Formatted price string
    """
    return f"${price:.2f}"


def format_menu_item(item: Dict[str, Any]) -> str:
    """
    Format a menu item for display

    Args:
        item: Menu item dictionary

    Returns:
        Formatted string representation
    """
    name = item.get('name', 'Unknown')
    price = item.get('price', 0)
    description = item.get('description', '')
    available = item.get('available', True)

    status = "✅ Available" if available else "❌ Out of stock"

    result = f"{name} - {format_price(price)} ({status})"
    if description:
        result += f"\n  {description}"

    return result


def format_order_summary(order: Dict[str, Any]) -> str:
    """
    Format an order for display

    Args:
        order: Order dictionary

    Returns:
        Formatted order summary string
    """
    lines = [
        "📋 Order Summary:",
        f"  Order ID: {order.get('id', 'N/A')}",
        f"  Customer: {order.get('customer_name', 'N/A')}",
        f"  Phone: {order.get('customer_phone', 'N/A')}",
    ]

    if order.get('table_number'):
        lines.append(f"  Table: {order['table_number']}")
    else:
        lines.append("  Type: Takeaway")

    lines.append("\n  Items:")
    items = order.get('items', [])
    total = 0

    for item in items:
        item_name = item.get('item_name', 'Unknown')
        quantity = item.get('quantity', 0)
        price = item.get('price', 0)
        subtotal = quantity * price
        total += subtotal

        lines.append(f"    • {quantity}x {item_name} - {format_price(subtotal)}")

        if item.get('notes'):
            lines.append(f"      Note: {item['notes']}")

    lines.append(f"\n  💰 Total: {format_price(total)}")

    if order.get('notes'):
        lines.append(f"  📝 Notes: {order['notes']}")

    lines.append(f"  Status: {order.get('status', 'pending').upper()}")

    return "\n".join(lines)


def test_api_connection() -> bool:
    """
    Test if the restaurant API is accessible

    Returns:
        True if API is accessible, False otherwise
    """
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/menu", timeout=5)
        return response.status_code == 200
    except Exception:
        return False