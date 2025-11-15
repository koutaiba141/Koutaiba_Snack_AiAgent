import app
from fastapi import FastAPI

app = FastAPI(
    title="Koutaiba Snack Restaurant Management System",
    description="A FastAPI backend for managing a restaurant, designed for LLM and MCP integration.",
    version="1.0.0",
)
from api.controllers import menu_controller, order_controller, inventory_controller, customer_controller


# Include routers
app.include_router(menu_controller.router, tags=["Menu"])
app.include_router(order_controller.router, tags=["Orders"])
app.include_router(inventory_controller.router, tags=["Inventory"])
app.include_router(customer_controller.router, tags=["Customer Analytics"])

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the Koutaiba Snack Restaurant Management System API"}

