#!/bin/bash
# 将 shared/js/v7-core.js 同步到 Web / Chrome / 小程序
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/shared/js/v7-core.js"

for dest in \
  "$ROOT/web/js/v7-core.js" \
  "$ROOT/chrome_extension/js/v7-core.js" \
  "$ROOT/miniprogram/utils/v7-core.js"; do
  mkdir -p "$(dirname "$dest")"
  cp "$SRC" "$dest"
  echo "✓ $dest"
done

echo "同步完成"
