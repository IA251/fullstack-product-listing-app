# /products/services/products_service.py
# Service layer responsible for products business logic and payload normalization.
from typing import Optional, Dict, Any, List
from math import ceil
from urllib.parse import quote


class ProductsService:
    """Service layer for products business logic."""

    def __init__(self, repository):
        self.repo = repository

    async def get_products(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Fetch paginated products from the repository."""
        try:
            page, limit, skip = self._build_pagination(page, limit)
            raw_data = await self.repo.get_products(limit=limit, skip=skip)
            products = self._normalize_products(raw_data.get("products", []))
            return self._build_response(products, raw_data, page, limit)
        except Exception as e:
            raise ProductsServiceException(str(e))

    async def search_products(self, query: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Search products by query text."""
        try:
            page, limit, skip = self._build_pagination(page, limit)
            raw_data = await self.repo.search_products(
                query=query,
                limit=limit,
                skip=skip
            )
            products = self._normalize_products(raw_data.get("products", []))
            return self._build_response(
                products,
                raw_data,
                page,
                limit,
                query=query
            )
        except Exception as e:
            raise ProductsServiceException(str(e))

    def _normalize_products(self, products: List[dict]) -> List[dict]:
        """Normalize raw product list for the frontend."""
        return [self._normalize_product(p) for p in products]

    def _normalize_product(self, p: dict) -> dict:
        """Normalize a single product record for the frontend."""
        images = p.get("images") or []
        return {
            "id": p.get("id"),
            "title": p.get("title"),
            "description": p.get("description"),
            "price": p.get("price"),
            "rating": p.get("rating"),
            "stock": p.get("stock"),
            "brand": p.get("brand"),
            "category": p.get("category"),
            "thumbnail": quote(p.get("thumbnail", ""), safe=":/"),
            "images": [quote(img, safe=":/") for img in images],
        }

    def _build_response(self, products: List[dict], raw_data: dict, page: int, limit: int, query: Optional[str] = None) -> Dict[str, Any]:
        """Build a common result payload with pagination."""

        total = raw_data.get("total", 0)
        total_pages = ceil(total / limit) if limit else 0

        response = {
            "items": products,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            }
        }

        if query is not None:
            response["query"] = query

        return response

    def _build_pagination(self, page: int, limit: int):
        """Normalize page/limit values and calculate skip."""
        page = max(page, 1)
        limit = max(limit, 1)
        skip = (page - 1) * limit
        return page, limit, skip

class ProductsServiceException(Exception):
    """Raised when the products service encounters an error."""
    pass