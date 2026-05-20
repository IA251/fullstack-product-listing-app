# /products/repositories/products_repository.py
# Repository layer that fetches products from the external API.
import httpx

class ProductsRepository:
    """Repository for fetching products from the external API."""

    BASE_URL = "https://dummyjson.com/products"

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_products(self, limit: int = 30, skip: int = 0) -> dict:
        """Fetch paginated products from the DummyJSON API."""
        limit, skip = self._validate_pagination(limit, skip)
        return await self._request(
            url=self.BASE_URL,
            params={"limit": limit, "skip": skip}
        )

    async def search_products(self ,query: str ,limit: int = 30 ,skip: int = 0) -> dict:
        """Search products using the API search endpoint."""
        limit, skip = self._validate_pagination(limit, skip)
        return await self._request(
            url=f"{self.BASE_URL}/search",
            params={
                "q": query,
                "limit": limit,
                "skip": skip
            }
        )

    async def _request(self, url: str, params: dict) -> dict:
        """Send a request and return JSON or raise a typed error."""
        try:
            res = await self.client.get(url, params=params)
            res.raise_for_status()
            return res.json()
        except httpx.RequestError as e:
            raise ProductsAPIException(f"Network error: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise ProductsAPIException(
                f"HTTP error {e.response.status_code}: {e.response.text[:200]}"
            )

    def _validate_pagination(self, limit: int, skip: int):
        """Ensure pagination parameters are valid."""
        if not isinstance(limit, int) or not isinstance(skip, int):
            raise ProductsValidationException(
                "limit and skip must be integers"
            )
        if limit <= 0:
            raise ProductsValidationException(
                "limit must be greater than 0"
            )
        if skip < 0:
            raise ProductsValidationException(
                "skip cannot be negative"
            )
        return limit, skip

class ProductsAPIException(Exception):
    """Base exception for product repository errors."""
    pass

class ProductsValidationException(ProductsAPIException):
    """Raised when product pagination input is invalid."""
    pass