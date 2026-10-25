from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total = 0
    order_items = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Product unavailable")
        
        total += product.price * item.quantity
        product.stock -= item.quantity
        order_items.append((product, item.quantity))
        
    order = Order(user_id=user.id, total_amount=total, status="placed")
    db.add(order)
    db.flush()
    
    for product, quantity in order_items:
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price))
    db.query(CartItem).filter(CartItem.user_id == user.id).delete(synchronize_session=False)
    db.commit()
    db.refresh(order)
    return {"message": "Order placed successfully", "order_id": order.id, "total_amount": total}




@router.get("/orders")
def get_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders