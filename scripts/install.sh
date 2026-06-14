#!/bin/bash
# A股反收割系统 v8 — 一键安装（任何人可用）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 A股反收割系统 v8 · 安装向导"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Python 版本检查
if ! command -v python3 &>/dev/null; then
  echo "❌ 未找到 python3，请先安装 Python 3.9+"
  echo "   macOS: brew install python3"
  echo "   或访问: https://www.python.org/downloads/"
  exit 1
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 9 ]; }; then
  echo "❌ 需要 Python 3.9+，当前: $PY_VER"
  exit 1
fi
echo "✓ Python $PY_VER"

# 虚拟环境（推荐，不污染系统）
if [ ! -d .venv ]; then
  echo "→ 创建虚拟环境 .venv ..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "✓ 虚拟环境已激活"

echo "→ 安装依赖 ..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ 依赖安装完成"

# 脚本权限 & 资源
chmod +x scripts/*.sh 2>/dev/null || true
./scripts/sync_js.sh
python3 scripts/generate_icons.py

echo "→ 运行测试 ..."
python3 -m unittest tests.test_v7 tests.test_v8 -v

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 安装成功！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  下一步（任选一种）："
echo ""
echo "  ./scripts/start.sh     交互式启动菜单"
echo "  make start             同上"
echo "  make run-v8            终端完整报告"
echo "  make dashboard         数据看板（浏览器）"
echo "  make web               网页版"
echo ""
echo "  在线 Web（GitHub Pages 部署后）："
echo "  https://shajindi-gif.github.io/a-stock-anti-extraction-v7/"
echo ""
