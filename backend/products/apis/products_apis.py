from contextlib import asynccontextmanager
from typing import Optional
import os

import httpx
from fastapi import FastAPI, Depends

from products.repositories.products_repository import ProductsRepository
from products.services.products_service import ProductsService
from products.schemas.products_schema import (
    ProductsResponseSchema,
    SearchProductsResponseSchema,
)


# manage shared async HTTP client for this FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # allow providing a path to a CA bundle via `SSL_CERT_FILE` env var
    ssl_cert = os.environ.get("SSL_CERT_FILE")
    if ssl_cert:
        async with httpx.AsyncClient(timeout=10.0, verify=ssl_cert) as client:
            app.state.http_client = client
            yield
    else:
        async with httpx.AsyncClient(timeout=10.0) as client:
            app.state.http_client = client
            yield


# FastAPI app instance with a lifespan that provides the httpx client
app = FastAPI(lifespan=lifespan)


def get_http_client() -> httpx.AsyncClient:
    """Return the shared HTTP client from app state."""
    return app.state.http_client


def get_products_service(
    http_client: httpx.AsyncClient = Depends(lambda: app.state.http_client),
) -> ProductsService:
    """Create a service instance with a request-scoped repository."""
    repo = ProductsRepository(client=http_client)
    return ProductsService(repository=repo)


@app.get("/products", response_model=ProductsResponseSchema)
async def get_products(
    page: int = 1,
    limit: int = 15,
    service: ProductsService = Depends(get_products_service),
):
    """Return paginated products."""
    return await service.get_products(page=page, limit=limit)


@app.get("/products/search", response_model=SearchProductsResponseSchema)
async def search_products(
    q: Optional[str] = None,
    page: int = 1,
    limit: int = 15,
    service: ProductsService = Depends(get_products_service),
):
    """Search products by text query."""
    return await service.search_products(query=q, page=page, limit=limit)
