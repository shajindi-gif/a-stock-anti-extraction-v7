#!/bin/bash
# 将 shared/js 核心同步到 Web / Chrome / 小程序
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

sync_file() {
  local src="$1"
  shift
  for dest in "$@"; do
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "✓ $dest"
  done
}

sync_file "$ROOT/shared/js/v7-core.js" \
  "$ROOT/web/js/v7-core.js" \
  "$ROOT/chrome_extension/js/v7-core.js" \
  "$ROOT/miniprogram/utils/v7-core.js"

sync_file "$ROOT/shared/js/v8-core.js" \
  "$ROOT/web/js/v8-core.js" \
  "$ROOT/chrome_extension/js/v8-core.js" \
  "$ROOT/miniprogram/utils/v8-core.js"

echo "同步完成（v7 + v8）"
