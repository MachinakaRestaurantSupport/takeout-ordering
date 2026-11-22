## Purpose

店外からの持ち帰り注文におけるSNS認証、公開メニュー参照、受取予約付き注文受付、注文状況確認、受取可能通知の各API仕様を定義する。これにより顧客の利便性向上と店頭混雑緩和を実現する。

## ADDED Requirements

### Requirement: SNS認証と持ち帰り注文フロー

システムはGoogle・Facebook・LINEのSNS認証、持ち帰りメニュー取得、I-2連携による受取予約注文、状況確認および受取可能通知をSHALL提供する。

#### Scenario: SNSログイン成功

- **WHEN** `POST /auth/login` に `google`、`facebook`、または `line` と有効なトークンを送信する
- **THEN** 顧客IDとアクセストークンを含む認証セッションを返却する

#### Scenario: 未対応プロバイダ拒否

- **WHEN** `POST /auth/login` に未対応プロバイダを送信する
- **THEN** ステータス 422 を返却する

#### Scenario: メニュー参照と予約注文・通知

- **WHEN** `GET /takeout/menus`、`POST /takeout/orders`、`GET /takeout/orders/{order_id}`、`POST /takeout/orders/{order_id}/notify-ready` を呼び出す
- **THEN** I-5/I-2連携結果および受取可能通知結果を返却する
