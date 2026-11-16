# Tasks: 持ち帰り注文（takeout-ordering）初期MVP

## 0. 初期セットアップ・仕様策定

- [x] 0.1 `.gitignore` 作成および初期ファイル・サブモジュール参照のコミット
- [x] 0.2 OpenSpec `init` 変更ドキュメント（`proposal.md`, `specs/takeout-flow/spec.md`, `design.md`, `tasks.md`）の作成と検証

## 1. プロジェクト基盤

- [x] 1.1 `pyproject.toml`（`name="takeout-ordering"`, pytest `pythonpath=["src"]`, ruff `line-length=100`）の作成

## 2. アプリケーション実装

- [x] 2.1 `src/takeout_ordering/__init__.py` および `models.py` の実装 [TakeoutOrdering_R01.DM01-01, TakeoutOrdering_R01.DM01-02, TakeoutOrdering_R01.DM01-03]
- [x] 2.2 `src/takeout_ordering/store.py`（SNS認証セッション・受取通知ストア）の実装 [TakeoutOrdering_R01.DM01-01, TakeoutOrdering_R01.DM01-03]
- [x] 2.3 `src/takeout_ordering/clients.py`（`MenuClient`, `OrderClient`）の実装 [TakeoutOrdering_R01.DM01-02, TakeoutOrdering_R01.DM01-03]
- [x] 2.4 `src/takeout_ordering/main.py`（FastAPI アプリと全エンドポイント）の実装 [TakeoutOrdering_R01.DM01-01, TakeoutOrdering_R01.DM01-02, TakeoutOrdering_R01.DM01-03]

## 3. 単体試験・品質検証

- [x] 3.1 `tests/test_takeout.py` の実装（`httpx.MockTransport` を用いた全フロー検証）および `pytest` 実行確認
