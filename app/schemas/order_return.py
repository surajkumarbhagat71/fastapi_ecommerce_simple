from pydantic import BaseModel


class OrderReturnCartCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderReturnCreate(BaseModel):
    order_id: int
    reason: str
    status: str | None = None
    order_return_cart: list[OrderReturnCartCreate] | None = None


class OrderReturnResponse(BaseModel):
    order_id: int
    message: str
    status: str
    

class OrderReturnListCartResponse(BaseModel):
    order_id: int
    reason: str
    status: str | None = None
    order_return_cart: list[OrderReturnCartCreate] | None = None
    model_config = {"from_attributes": True}


    
