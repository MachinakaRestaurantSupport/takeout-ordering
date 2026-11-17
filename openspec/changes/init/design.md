# Design: 持ち帰り注文（takeout-ordering）初期MVP

## アーキテクチャ

- **言語・フレームワーク**: Python 3.12 + FastAPI + Pydantic v2 + httpx
- **モジュール構成**:
  - `src/takeout_ordering/__init__.py`: パッケージ公開エントリポイント
  - `src/takeout_ordering/models.py`: リクエスト／レスポンス用 Pydantic モデル定義
  - `src/takeout_ordering/store.py`: 認証セッションおよび受取可能通知履歴のインメモリストア
  - `src/takeout_ordering/clients.py`: `MenuClient`（I-5連携）および `OrderClient`（I-2連携）。`httpx.Client` に `base_url` / `transport` を注入可能とし、単体試験時の `httpx.MockTransport` および結合試験時の `httpx.ASGITransport` に対応
  - `src/takeout_ordering/main.py`: `create_app(menu_client=None, order_client=None)` ファクトリと `app = create_app()`

## API エンドポイント設計

- `GET /health` -> `200`: `{"status": "ok", "service": "takeout-ordering"}`
- `POST /auth/login` -> `200`: `provider` (`google` | `facebook` | `line`), `oauth_token` (`min_length=1`), `display_name` (default `"Guest"`) を受け取り、`customer_id`, `provider`, `display_name`, `access_token` を返却。未対応プロバイダや空トークンは Pydantic により `422` を返却。
- `GET /takeout/menus` -> `200`: `MenuClient.get_takeout_menus()` で `GET /menus/takeout` を呼び出し返却。
- `POST /takeout/orders` -> `201`: `customer_id`, `pickup_at`, `items` を受け取り、`OrderClient.create_takeout_order()` で `POST /orders` (`source="takeout"`) を呼び出し、結果を `201` で返却。
- `GET /takeout/orders/{order_id}` -> `200`: `OrderClient.get_order(order_id)` で `GET /orders/{order_id}` を呼び出し返却。
- `POST /takeout/orders/{order_id}/notify-ready` -> `200`: ストアに受取可能通知を記録し、`{"order_id": order_id, "notified": True, "message": "ご注文の品の準備が整いました"}` を返却。

## USDM 要求ID トレーサビリティ

| USDM 要求ID | 要求内容 | 対応エンドポイント / モジュール |
| --- | --- | --- |
| `TakeoutOrdering_R01.DM01-01` | `POST /auth/login` で `google` / `facebook` / `line` プロバイダの認証セッションを発行できる | `POST /auth/login` (`models.py`, `store.py`, `main.py`) |
| `TakeoutOrdering_R01.DM01-02` | `POST /takeout/orders` で受取予約時刻付き注文を受け付け、注文管理（I-2）へ連携できる | `GET /takeout/menus`, `POST /takeout/orders` (`models.py`, `clients.py`, `main.py`) |
| `TakeoutOrdering_R01.DM01-03` | `GET /takeout/orders/{order_id}` および `POST /takeout/orders/{order_id}/notify-ready` で状況確認と受取可能通知を処理できる | `GET /takeout/orders/{order_id}`, `POST /takeout/orders/{order_id}/notify-ready` (`clients.py`, `store.py`, `main.py`) |
