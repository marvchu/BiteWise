from fastapi import FastAPI

from routers import homepage, menu_items, restaurants

app = FastAPI(title="BiteWise API")

app.include_router(homepage.router)
app.include_router(menu_items.router)
app.include_router(restaurants.router)
