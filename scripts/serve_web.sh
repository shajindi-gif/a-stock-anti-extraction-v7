#!/bin/bash
# 启动本地 Web Demo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8080}"
echo "🌐 Web Demo: http://localhost:$PORT/web/"
echo "   按 Ctrl+C 停止"
cd "$ROOT"
python3 -m http.server "$PORT"
