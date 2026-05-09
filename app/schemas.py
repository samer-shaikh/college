from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    name: str
    price: int
    description: str | None = None

class ProductOut(ProductCreate):
    id: int
    name: str
    price: int
    description: str
    image: str

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    data: List[ProductOut]
    total: int
    page: int
    limit: int

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[CartItemCreate]

class OrderOut(BaseModel):
    id: int
    total: int
    class Config:
        from_attributes = True