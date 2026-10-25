from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.order import Order, OrderReturn, OrderReturnCart
from app.models.user import User
from app.schemas.order_return import OrderReturnCreate, OrderReturnResponse , OrderReturnListCartResponse
from app.models.product import Product


router = APIRouter(prefix="/order-returns", tags=["Order Returns"])


@router.post("/", response_model=OrderReturnResponse)
def create_order_return(data: OrderReturnCreate,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    print('userid',user.id)
    order = db.query(Order).filter(Order.id == data.order_id,Order.user_id == user.id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    existing_return = db.query(OrderReturn.id).filter(OrderReturn.order_id == data.order_id).first()
    
    if existing_return:
        raise HTTPException(status_code=400, detail="Order return already exists")

    order_return = OrderReturn(order_id=data.order_id,user_id = user.id , reason=data.reason,status=data.status or "pending")
    db.add(order_return)
    db.flush()

    for x in data.order_return_cart or []:
        order_return_cart = OrderReturnCart(
            user_id=user.id,
            product_id=x.product_id,
            quantity=x.quantity,
            order_return_id=order_return.id,
        )
        db.add(order_return_cart)
        
        get_product = db.query(Product).filter(Product.id == x.product_id).first()
        get_product.stock += x.quantity
        
    db.commit()
    db.refresh(order_return)
    
    data = {
        "order_id": order_return.order_id,
        'message': "Order return created successfully",
        "status": order_return.status,
    }
    return data
    

@router.get("/delete/{order_return_id}")
def delete_order_return(order_return_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order_return = db.query(OrderReturn).filter(OrderReturn.id == order_return_id, OrderReturn.user_id == user.id).first()
    
    if not order_return:
        raise HTTPException(status_code=404, detail="Order return not found")
    
    order_return_carts = db.query(OrderReturnCart).filter(OrderReturnCart.order_return_id == order_return_id).all()
    
    for cart in order_return_carts:
        product = db.query(Product).filter(Product.id == cart.product_id).first()
        if product:
            product.stock -= cart.quantity
        db.delete(cart)

    db.flush()
    db.delete(order_return)
    db.commit()
    return {"message": "Order return deleted successfully"}


@router.get("/order-returns", response_model=list[OrderReturnListCartResponse])
def get_order_returns(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order_returns = db.query(OrderReturn).filter(OrderReturn.user_id == user.id).all()
    return order_returns



