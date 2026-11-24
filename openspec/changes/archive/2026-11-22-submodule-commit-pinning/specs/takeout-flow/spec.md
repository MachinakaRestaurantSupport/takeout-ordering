# Spec: takeout-flow

## ADDED Requirements

### Requirement: サブモジュール参照のコミット指定管理

本リポジトリは `.gitmodules` に `branch` 設定を持たせず `reference/system-integration` を確定コミット SHA（gitlink）指定で管理しなければならず（MUST）、`reference/system-integration/` 配下を読み取り専用として直接変更してはならない（SHALL）。

#### Scenario: サブモジュール参照の更新とマージ

- **WHEN** `system-integration` の確定コミット SHA（`<commit-sha>`）を `reference/system-integration` にチェックアウトし、`system-integration` PR の Merge commit マージ後に本リポジトリの PR を `main` にマージするとき
- **THEN** `.gitmodules` の書き換えやマージ後の `main` 戻し作業なしで、正しい仕様・画像参照を維持したままマージが完了する（SHALL）
