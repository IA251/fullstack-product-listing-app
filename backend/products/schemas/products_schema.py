# /products/schemas/products_schema.py
from pydantic import BaseModel
from typing import Optional, List

# Product Schema
class ProductSchema(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = []

# Pagination Schema
class PaginationSchema(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

# Products Response Schema
class ProductsResponseSchema(BaseModel):
    items: List[ProductSchema]
    pagination: PaginationSchema

# Search Response Schema
class SearchProductsResponseSchema(BaseModel):
    query: Optional[str] = None
    items: List[ProductSchema]
    pagination: PaginationSchema
