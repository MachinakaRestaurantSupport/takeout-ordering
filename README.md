# takeout-ordering

Google・Facebook・LINEログインに対応し、店外からの持ち帰り事前注文、受取時刻予約、注文状況確認、受取可能通知を提供するツールです。  
メニュー管理・注文管理（I-2, I-5）および店長・スタッフ共通ポータル（[ポータル画面イメージ](reference/system-integration/docs/images/portal/01-portal-dashboard.png)）と連携します。

## 画面遷移図

縮小画面キャプチャを用いた `takeout-ordering` の画面遷移図です（draw.io 編集用ソース: [transition.drawio](reference/system-integration/docs/images/takeout_ordering/transition.drawio)）。

![takeout-ordering 画面遷移図](reference/system-integration/docs/images/takeout_ordering/transition.svg)

## 代表機能イメージ

### 1. SNS認証ログイン (`GET /ui/takeout/login`)
Google / Facebook / LINE のSNSログインに対応した認証画面と、現在アクティブな顧客セッション一覧を表示します。

![SNS認証ログイン](reference/system-integration/docs/images/takeout_ordering/01-sns-login.png)

### 2. メニュー選択・受取時刻予約 (`GET /ui/takeout/reserve`)
持ち帰り専用メニュー（`takeout` チャネル）の商品一覧を参照し、店頭での受取希望時刻を指定して事前注文（`POST /takeout/orders`）を行います。

![メニュー選択・受取時刻予約](reference/system-integration/docs/images/takeout_ordering/02-takeout-reserve.png)

### 3. 注文状況確認・受取可能通知 (`GET /ui/takeout/status`)
予約注文の調理状況（注文管理連携）および「ご注文の品の準備が整いました」の受取可能通知履歴（`POST /takeout/orders/{order_id}/notify-ready`）を確認できます。

![注文状況・受取可能通知](reference/system-integration/docs/images/takeout_ordering/03-pickup-notification.png)

## 提供 API・UI エンドポイント

| 種別 | メソッド & パス | 機能概要 |
|---|---|---|
| API | `GET /health` | ヘルスチェック |
| API | `POST /auth/login` | SNSプロバイダ認証セッション発行 |
| API | `GET /takeout/menus` | 持ち帰り公開メニュー取得 (I-5) |
| API | `POST /takeout/orders` | 受取予約付き持ち帰り注文作成 (I-2) |
| API | `GET /takeout/orders/{order_id}` | 予約注文ステータス取得 |
| API | `POST /takeout/orders/{order_id}/notify-ready` | 受取可能通知の記録・配信 |
| UI | `GET /ui/takeout/login` | SNS認証ログイン画面 |
| UI | `GET /ui/takeout/reserve` | メニュー選択・受取予約画面 |
| UI | `GET /ui/takeout/status` | 注文状況・受取可能通知画面 |

## テスト・静的解析の実行

```bash
../.venv/bin/python3 -m pytest -v
../.venv/bin/ruff check .
```
