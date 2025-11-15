
from api.database.supabase_conn import supabase
from api.models import schemas
from typing import List

async def get_all_customers() -> List[schemas.Customer]:
    response = supabase.from_("orders").select("customer_name", "customer_phone").execute()
    return [schemas.Customer(**row) for row in response.data]

async def get_popular_items() -> List[schemas.PopularItem]:
    response = supabase.from_("order_items").select("item_id, items(name)").execute()
    item_counts = {}
    for row in response.data:
        item_id = row['item_id']
        item_name = row['items']['name']
        if item_id not in item_counts:
            item_counts[item_id] = {"name": item_name, "total_orders": 0}
        item_counts[item_id]["total_orders"] += 1

    popular_items = sorted(item_counts.items(), key=lambda x: x[1]['total_orders'], reverse=True)[:10]

    return [schemas.PopularItem(item_id=item_id, name=data['name'], total_orders=data['total_orders']) for item_id, data in popular_items]

async def get_revenue_stats() -> schemas.RevenueStats:
    from datetime import datetime, timedelta

    now = datetime.now()
    one_day_ago = now - timedelta(days=1)
    one_week_ago = now - timedelta(weeks=1)
    one_month_ago = now - timedelta(days=30)

    daily_revenue = supabase.from_("orders").select("total_amount").gte("created_at", one_day_ago.isoformat()).execute()
    weekly_revenue = supabase.from_("orders").select("total_amount").gte("created_at", one_week_ago.isoformat()).execute()
    monthly_revenue = supabase.from_("orders").select("total_amount").gte("created_at", one_month_ago.isoformat()).execute()

    daily = sum([row['total_amount'] for row in daily_revenue.data])
    weekly = sum([row['total_amount'] for row in weekly_revenue.data])
    monthly = sum([row['total_amount'] for row in monthly_revenue.data])

    return schemas.RevenueStats(daily=daily, weekly=weekly, monthly=monthly)
