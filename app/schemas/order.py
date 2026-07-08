from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrderItemCreate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    external_order_id: str = Field(..., min_length=2, max_length=50)
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailStr
    total: float = Field(..., gt=0)
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_order_id: str
    customer_name: str
    customer_email: str
    total: float
    status: str
    items: list[OrderItemResponse]
