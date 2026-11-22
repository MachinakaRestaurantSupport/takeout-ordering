# Tasks: reference/system-integration のコミット指定化とルール統一

- [x] 1.1 `.gitmodules` から `branch` 行を削除して `path` と `url` のみのコミット SHA 指定構成にする
- [x] 1.2 `AGENTS.md`・`openspec/config.yaml`・OpenSpec スキル定義（`.agents/`, `.cline/`, `.github/`, `.hermes/`）の submodule 手順を確定コミット SHA 指定および `system-integration` 先行 Merge commit 固定に統一する
- [x] 1.3 `reference/system-integration` を `system-integration` の `feature/submodule-commit-pinning` 最新コミット SHA へ更新し、`pytest -q`・`ruff check .`・`openspec archive submodule-commit-pinning -y` を完了する
