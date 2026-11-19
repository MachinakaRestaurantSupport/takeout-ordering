"""HTTP clients for menu-management (I-5) and order-management (I-2)."""

from typing import Any

import httpx


class MenuClient:
    """Client for retrieving takeout menus from menu-management (I-5)."""

    def __init__(
        self,
        base_url: str = "http://menu-management",
        transport: httpx.BaseTransport | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client(base_url=base_url, transport=transport)

    def get_takeout_menus(self) -> Any:
        """Fetch published takeout menus via GET /menus/takeout."""
        response = self._client.get("/menus/takeout")
        response.raise_for_status()
        return response.json()


class ProductClient:
    """Client for retrieving master product details from product-management."""

    def __init__(
        self,
        base_url: str = "http://product-management",
        transport: httpx.BaseTransport | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client(base_url=base_url, transport=transport)

    def get_product(self, product_id: str) -> dict[str, Any] | None:
        """Fetch product details via GET /products/{product_id}; return None if not found."""
        response = self._client.get(f"/products/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


class OrderClient:
    """Client for creating and querying takeout orders in order-management (I-2)."""

    def __init__(
        self,
        base_url: str = "http://order-management",
        transport: httpx.BaseTransport | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client(base_url=base_url, transport=transport)

    def create_takeout_order(
        self,
        customer_id: str,
        pickup_at: str,
        items: list[dict[str, Any]],
    ) -> Any:
        """Create a takeout order via POST /orders with source='takeout'."""
        payload = {
            "source": "takeout",
            "customer_id": customer_id,
            "pickup_at": pickup_at,
            "items": items,
        }
        response = self._client.post("/orders", json=payload)
        response.raise_for_status()
        return response.json()

    def get_order(self, order_id: str) -> Any:
        """Fetch an order's current status via GET /orders/{order_id}."""
        response = self._client.get(f"/orders/{order_id}")
        response.raise_for_status()
        return response.json()

    def list_orders(self) -> list[dict[str, Any]]:
        """Fetch all orders via GET /orders."""
        response = self._client.get("/orders")
        response.raise_for_status()
        return response.json()
