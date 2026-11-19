from pydantic import BaseModel, Field
from typing import Literal

class ProductCreate(BaseModel):
    sku: str | None = None
    name: str = Field(min_length=1, max_length=160)
    category: str = Field(default="Général", max_length=100)
    unit: str = Field(default="unité", max_length=30)
    purchase_price: int = Field(default=0, ge=0)
    sale_price: int = Field(ge=0)
    stock: float = Field(default=0, ge=0)

class SaleLine(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)

class SaleCreate(BaseModel):
    channel: Literal["restaurant", "commerce"]
    items: list[SaleLine] = Field(min_length=1)
    discount: int = Field(default=0, ge=0)
    payment_method: str = Field(default="espèces", max_length=40)
