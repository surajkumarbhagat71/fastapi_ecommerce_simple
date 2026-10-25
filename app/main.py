from fastapi import FastAPI
from app.api.category import router as category_router
from app.api.product import router as product_router
from app.api.auth import router as auth_router
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.api.order_return import router as order_return_router

app = FastAPI(title="Simple FastAPI E-Commerce")

app.include_router(category_router)
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(order_return_router)

@app.get("/health")
def health():
    return {"status": "ok"}
