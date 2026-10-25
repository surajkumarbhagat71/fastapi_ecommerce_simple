from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_to_cart(data: CartCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    item = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.product_id == data.product_id).first()
    if item:
        item.quantity += data.quantity
    else:
        db.add(CartItem(user_id=user.id, product_id=data.product_id, quantity=data.quantity))
    db.commit()
    return {"message": "Product added to cart"}
