# AGENTS.md — 持ち帰り注文（takeout-ordering）

MachinakaRestaurantSupportTools のサブシステム「持ち帰り注文」のリポジトリ。

## 参照（git submodule・読み取り専用）

- `reference/system-integration/`: 全体システムの仕様・設計
  - 当該ツールの USDM: `reference/system-integration/usdm/takeout_ordering/`
  - 全体 USDM / 全体システム設計: `reference/system-integration/docs/system-design.md`

## opsx フロー

1. **opsx:propose**: `system-integration` と揃えた `feature/<change-id>` ブランチを作成し、`.gitmodules`（`branch` 指定なし）は変更せず `reference/system-integration` に対象コミット SHA（`<commit-sha>`）をチェックアウトして gitlink を更新
   ```bash
   git checkout -b feature/<change-id>
   git -C reference/system-integration fetch origin feature/<change-id>
   git -C reference/system-integration checkout <commit-sha>
   git add reference/system-integration
   ```
2. OpenSpec でソフトウェア設計（design.md）とモジュールごとの WHEN/THEN 詳細設計（specs/<module>/spec.md）を作成
3. **opsx:apply**: 実装 → 単体試験（全テストパス必須。実行結果を報告）
4. **opsx:archive**: `openspec archive <change-id> -y` を完了した上で、結合試験・全 PR レビュー完了後に `system-integration` PR（`Create a merge commit` 固定）へ続けて本リポジトリの PR を `main` へマージ（submodule はコミット SHA 指定のため、マージ後の参照戻し作業は不要）

## ルール

- `reference/system-integration/` 配下は変更しない（正本は system-integration 側。仕様の問題はユーザーに報告し、system-integration での変更提案を提示）
- エージェントワークフロー中に git commit を実行しない（PR 作成・コミットもユーザーの明示的指示後に実行）
