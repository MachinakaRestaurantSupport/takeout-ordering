# takeout-flow Specification

## Purpose
店外からの持ち帰り注文におけるSNS認証、公開メニュー参照、受取予約付き注文受付、注文状況確認、受取可能通知の各API仕様を定義する。これにより顧客の利便性向上と店頭混雑緩和を実現する。

## Requirements

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

### Requirement: サブモジュール参照のコミット指定管理

本リポジトリは `.gitmodules` に `branch` 設定を持たせず `reference/system-integration` を確定コミット SHA（gitlink）指定で管理しなければならず（MUST）、`reference/system-integration/` 配下を読み取り専用として直接変更してはならない（SHALL）。

#### Scenario: サブモジュール参照の更新とマージ

- **WHEN** `system-integration` の確定コミット SHA（`<commit-sha>`）を `reference/system-integration` にチェックアウトし、`system-integration` PR の Merge commit マージ後に本リポジトリの PR を `main` にマージするとき
- **THEN** `.gitmodules` の書き換えやマージ後の `main` 戻し作業なしで、正しい仕様・画像参照を維持したままマージが完了する（SHALL）
