# Proposal: 持ち帰り注文（takeout-ordering）初期MVP実装

## 背景と目的

USDM要求 `TakeoutOrdering_R01`（店外持ち帰り注文管理）および全体システム設計（`reference/system-integration/docs/system-design.md`）に基づき、店外からの持ち帰り注文を支える初期MVP APIを構築する。

## スコープ

- `GET /health`: ヘルスチェック
- `POST /auth/login`: Google / Facebook / LINE のSNSプロバイダ認証セッション発行（未対応プロバイダは HTTP 422）
- `GET /takeout/menus`: メニュー管理（I-5）連携による持ち帰りメニュー取得
- `POST /takeout/orders`: 受取予約時刻付き事前注文の受付と注文管理（I-2）連携
- `GET /takeout/orders/{order_id}`: 注文管理（I-2）連携による注文状況確認
- `POST /takeout/orders/{order_id}/notify-ready`: 受取可能通知の記録および応答
- `tests/test_takeout.py`: `httpx.MockTransport` を用いた単体試験

## スコープ外

- 本番SNS OAuthプロバイダとの外部トークン検証通信
- 実際のプッシュ通知・メール・LINEメッセージ送信基盤との連携
- サブシステム間結合試験（`system-integration` 側で実施）
