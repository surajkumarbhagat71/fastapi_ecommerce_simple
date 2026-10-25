from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    category_id: int

class ProductResponse(ProductCreate):
    id: int
    is_active: bool
    class Config:
        from_attributes = True
