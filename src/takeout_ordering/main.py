"""FastAPI application for the takeout-ordering subsystem."""

from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, status

from takeout_ordering.clients import MenuClient, OrderClient
from takeout_ordering.models import (
    LoginRequest,
    LoginResponse,
    NotifyReadyResponse,
    TakeoutOrderRequest,
)
from takeout_ordering.store import TakeoutStore


def create_app(
    menu_client: MenuClient | None = None,
    order_client: OrderClient | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Takeout Ordering Service", version="0.1.0")
    resolved_menu_client = menu_client or MenuClient()
    resolved_order_client = order_client or OrderClient()
    store = TakeoutStore()
    app.state.store = store

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "takeout-ordering"}

    @app.post("/auth/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
    def login(payload: LoginRequest) -> LoginResponse:
        return store.create_session(
            provider=payload.provider,
            oauth_token=payload.oauth_token,
            display_name=payload.display_name,
        )

    @app.get("/takeout/menus")
    def get_takeout_menus() -> Any:
        try:
            return resolved_menu_client.get_takeout_menus()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

    @app.post("/takeout/orders", status_code=status.HTTP_201_CREATED)
    def create_takeout_order(payload: TakeoutOrderRequest) -> Any:
        items_payload = [item.model_dump() for item in payload.items]
        try:
            return resolved_order_client.create_takeout_order(
                customer_id=payload.customer_id,
                pickup_at=payload.pickup_at,
                items=items_payload,
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

    @app.get("/takeout/orders/{order_id}")
    def get_takeout_order(order_id: str) -> Any:
        try:
            return resolved_order_client.get_order(order_id)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

    @app.post(
        "/takeout/orders/{order_id}/notify-ready",
        response_model=NotifyReadyResponse,
        status_code=status.HTTP_200_OK,
    )
    def notify_ready(order_id: str) -> NotifyReadyResponse:
        return store.record_ready_notification(order_id)

    return app


app = create_app()
