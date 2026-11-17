"""Unit tests for takeout-ordering API using httpx.MockTransport."""

import json

import httpx
import pytest
from fastapi.testclient import TestClient

from takeout_ordering.clients import MenuClient, OrderClient, ProductClient
from takeout_ordering.main import create_app


def _build_test_client(
    captured_order_requests: list[dict] | None = None,
) -> TestClient:
    def menu_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and request.url.path == "/menus/takeout":
            return httpx.Response(
                200,
                json={
                    "channel": "takeout",
                    "items": [
                        {"product_id": "prod-1", "name": "唐揚げ弁当", "price": 850},
                        {"product_id": "prod-2", "name": "焼き魚弁当", "price": 900},
                    ],
                },
            )
        return httpx.Response(404, json={"detail": "Not found"})

    def order_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/orders":
            body = json.loads(request.content.decode("utf-8"))
            if captured_order_requests is not None:
                captured_order_requests.append(body)
            return httpx.Response(
                201,
                json={
                    "order_id": "ord-1001",
                    "source": body["source"],
                    "customer_id": body["customer_id"],
                    "pickup_at": body["pickup_at"],
                    "items": body["items"],
                    "status": "received",
                },
            )
        if request.method == "GET" and request.url.path == "/orders/ord-1001":
            return httpx.Response(
                200,
                json={
                    "order_id": "ord-1001",
                    "source": "takeout",
                    "status": "preparing",
                    "pickup_at": "2026-11-16T18:30:00+09:00",
                },
            )
        return httpx.Response(404, json={"detail": "Order not found"})

    products = {
        "prod-1": {"id": "prod-1", "name": "唐揚げ弁当", "price": 850, "takeout_available": True},
        "prod-2": {"id": "prod-2", "name": "焼き魚弁当", "price": 900, "takeout_available": True},
        "prod-dine": {
            "id": "prod-dine",
            "name": "特製ラーメン",
            "price": 980,
            "takeout_available": False,
        },
    }

    def product_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and request.url.path.startswith("/products/"):
            product_id = request.url.path.removeprefix("/products/")
            if product_id not in products:
                return httpx.Response(404, json={"detail": "Product not found"})
            return httpx.Response(200, json=products[product_id])
        return httpx.Response(404, json={"detail": "Not found"})

    menu_client = MenuClient(transport=httpx.MockTransport(menu_handler))
    order_client = OrderClient(transport=httpx.MockTransport(order_handler))
    product_client = ProductClient(transport=httpx.MockTransport(product_handler))
    app = create_app(
        menu_client=menu_client,
        order_client=order_client,
        product_client=product_client,
    )
    return TestClient(app)


def test_health() -> None:
    client = _build_test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "takeout-ordering"}


@pytest.mark.parametrize("provider", ["google", "facebook", "line"])
def test_sns_login_success(provider: str) -> None:
    client = _build_test_client()
    response = client.post(
        "/auth/login",
        json={
            "provider": provider,
            "oauth_token": "valid-token-123",
            "display_name": "Taro",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == provider
    assert data["display_name"] == "Taro"
    assert data["customer_id"].startswith(f"cust-{provider}-")
    assert data["access_token"].startswith("tok-")


def test_sns_login_default_display_name() -> None:
    client = _build_test_client()
    response = client.post(
        "/auth/login",
        json={"provider": "google", "oauth_token": "valid-token-abc"},
    )
    assert response.status_code == 200
    assert response.json()["display_name"] == "Guest"


def test_sns_login_invalid_provider_rejected() -> None:
    client = _build_test_client()
    response = client.post(
        "/auth/login",
        json={"provider": "twitter", "oauth_token": "valid-token-123"},
    )
    assert response.status_code == 422


def test_sns_login_empty_token_rejected() -> None:
    client = _build_test_client()
    response = client.post(
        "/auth/login",
        json={"provider": "line", "oauth_token": ""},
    )
    assert response.status_code == 422


def test_get_takeout_menus() -> None:
    client = _build_test_client()
    response = client.get("/takeout/menus")
    assert response.status_code == 200
    data = response.json()
    assert data["channel"] == "takeout"
    assert len(data["items"]) == 2
    assert data["items"][0]["product_id"] == "prod-1"


def test_create_and_get_takeout_order() -> None:
    captured: list[dict] = []
    client = _build_test_client(captured_order_requests=captured)

    create_resp = client.post(
        "/takeout/orders",
        json={
            "customer_id": "cust-line-001",
            "pickup_at": "2026-11-16T18:30:00+09:00",
            "items": [{"product_id": "prod-1", "quantity": 2}],
        },
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["order_id"] == "ord-1001"
    assert created["source"] == "takeout"
    assert len(captured) == 1
    assert captured[0]["source"] == "takeout"
    assert captured[0]["pickup_at"] == "2026-11-16T18:30:00+09:00"

    get_resp = client.get("/takeout/orders/ord-1001")
    assert get_resp.status_code == 200
    assert get_resp.json()["status"] == "preparing"


def test_notify_ready() -> None:
    client = _build_test_client()
    response = client.post("/takeout/orders/ord-1001/notify-ready")
    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ord-1001",
        "notified": True,
        "message": "ご注文の品の準備が整いました",
    }
    assert len(client.app.state.store.notifications) == 1
    assert client.app.state.store.notifications[0]["order_id"] == "ord-1001"


def test_takeout_ui_screens() -> None:
    client = _build_test_client()
    for path in ("/ui/takeout/login", "/ui/takeout/reserve", "/ui/takeout/status"):
        res = client.get(path)
        assert res.status_code == 200
        assert "持ち帰り注文" in res.text


def test_takeout_order_overrides_client_unit_price_with_master_price() -> None:
    captured: list[dict] = []
    client = _build_test_client(captured_order_requests=captured)

    resp = client.post(
        "/takeout/orders",
        json={
            "customer_id": "cust-line-001",
            "pickup_at": "2026-11-16T18:30:00+09:00",
            "items": [{"product_id": "prod-1", "unit_price": 10, "quantity": 2}],
        },
    )
    assert resp.status_code == 201
    assert captured[0]["items"] == [
        {
            "product_id": "prod-1",
            "product_name": "唐揚げ弁当",
            "unit_price": 850,
            "quantity": 2,
        }
    ]


def test_takeout_order_unknown_product_returns_404() -> None:
    client = _build_test_client()
    resp = client.post(
        "/takeout/orders",
        json={
            "customer_id": "cust-line-001",
            "pickup_at": "2026-11-16T18:30:00+09:00",
            "items": [{"product_id": "missing", "quantity": 1}],
        },
    )
    assert resp.status_code == 404


def test_takeout_order_unavailable_product_returns_422() -> None:
    client = _build_test_client()
    resp = client.post(
        "/takeout/orders",
        json={
            "customer_id": "cust-line-001",
            "pickup_at": "2026-11-16T18:30:00+09:00",
            "items": [{"product_id": "prod-dine", "quantity": 1}],
        },
    )
    assert resp.status_code == 422
