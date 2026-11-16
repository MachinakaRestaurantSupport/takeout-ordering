# AGENTS.md — 持ち帰り注文（takeout-ordering）

MachinakaRestaurantSupportTools のサブシステム「持ち帰り注文」のリポジトリ。

## 参照（git submodule・読み取り専用）

- `reference/system-integration/`: 全体システムの仕様・設計
  - 当該ツールの USDM: `reference/system-integration/usdm/takeout_ordering/`
  - 全体 USDM / 全体システム設計: `reference/system-integration/docs/system-design.md`

## opsx フロー

1. **opsx:propose**: system-integration の feature ブランチに合わせた `feature/<change-id>` を作成し、サブモジュール参照先ブランチも同名へ切り替え
   ```bash
   git checkout -b feature/<change-id>
   git config -f .gitmodules submodule.reference/system-integration.branch feature/<change-id>
   git submodule update --remote reference/system-integration
   ```
2. OpenSpec でソフトウェア設計（design.md）とモジュールごとの WHEN/THEN 詳細設計（specs/<module>/spec.md）を作成
3. **opsx:apply**: 実装 → 単体試験（全テストパス必須。実行結果を報告）
4. **opsx:archive**: このリポジトリの main への GitHub プルリクエスト作成。PR マージ時はファイル一覧の更新とサブモジュール参照ブランチを main に戻す
   ```bash
   git config -f .gitmodules submodule.reference/system-integration.branch main
   git submodule update --remote reference/system-integration
   git add .gitmodules reference/system-integration
   ```

## ルール

- `reference/system-integration/` 配下は変更しない（正本は system-integration 側。仕様の問題はユーザーに報告し、system-integration での変更提案を提示）
- エージェントワークフロー中に git commit を実行しない（PR 作成・コミットもユーザーの明示的指示後に実行）
