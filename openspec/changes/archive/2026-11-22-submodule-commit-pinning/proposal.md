# Proposal: reference/system-integration のコミット指定化と開発ルール統一

## Why

従来は作業ブランチごとに `.gitmodules` の `branch` を `feature/<change-id>` へ書き換え、PR マージ後に `main` へ戻す二度手間が生じていた。`.gitmodules` から `branch` 設定を廃止してコミット SHA 指定に統一し、`takeout-ordering`（持ち帰り注文）の運用記述を最新化する。

## What Changes

- `.gitmodules` から `branch = ...` 行を削除し、`path` と `url` のみのコミット指定管理へ統一する
- `AGENTS.md`、`openspec/config.yaml`、および `.agents/`・`.cline/`・`.github/`・`.hermes/` 配下の OpenSpec スキル定義を確定コミット SHA 指定および `system-integration` 先行 Merge commit 手順に更新する
- `reference/system-integration` を `system-integration` の確定コミット SHA へ更新する

## Capabilities

### New Capabilities

### Modified Capabilities
- `takeout-flow`: サブモジュール参照のコミット SHA 指定と読み取り専用運用要件を追加する。

## Impact

- `.gitmodules`, `AGENTS.md`, `openspec/config.yaml`, `.agents/skills/*/SKILL.md`, `.cline/skills/*/SKILL.md`, `.github/skills/*/SKILL.md`, `.hermes/skills/*/SKILL.md`, `reference/system-integration`
