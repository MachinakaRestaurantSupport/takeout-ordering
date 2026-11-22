# Design: サブモジュール参照のコミット指定化とルール統一（takeout-ordering）

## Context

全体仕様（USDM `R05` / `R05-01`：`S05-01-01`, `S05-01-02`）に基づき、`reference/system-integration` サブモジュール管理をブランチ指定からコミット SHA（gitlink）指定へ統一する。

## Goals / Non-Goals

- **Goals**:
  - `.gitmodules` から `branch` 行を削除し、常に `path` と `url` のみにする（`S05-01-01`）。
  - `AGENTS.md`・`openspec/config.yaml`・各種 OpenSpec スキル定義から `git config -f .gitmodules` や `--remote` 更新手順を廃止し、確定 `<commit-sha>` チェックアウト＋`system-integration` 先行 Merge commit 固定手順に揃える（`S05-01-02`）。
- **Non-Goals**:
  - `src/` 配下のアプリケーション API・UI ロジック変更および `reference/system-integration/` 配下の直接編集は行わない。

## USDM Traceability

- `R05` / `R05-01` (`S05-01-01`): `.gitmodules` の `branch` 設定廃止と確定 SHA 指定
- `R05` / `R05-01` (`S05-01-02`): サブシステム内ルール・設定・スキル定義の統一
