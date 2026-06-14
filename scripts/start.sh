#!/bin/bash
# A股反收割系统 v8 — 交互式启动器
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

show_menu() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  🚀 A股反收割系统 v8 · 启动菜单"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "  1) 终端报告 (v8 完整分析 + 东财条件单)"
  echo "  2) 数据看板 (Streamlit 可视化)"
  echo "  3) 网页版   (浏览器 http://localhost:8080/web/)"
  echo "  4) Mac 桌面 (图形界面)"
  echo "  5) 全场景 Demo (4 个场景批量)"
  echo "  6) 运行测试"
  echo "  7) Chrome 插件安装说明"
  echo "  0) 退出"
  echo ""
}

chrome_help() {
  echo ""
  echo "Chrome 插件安装（一次性）："
  echo "  1. 浏览器打开 chrome://extensions/"
  echo "  2. 开启「开发者模式」"
  echo "  3. 「加载已解压的扩展程序」"
  echo "  4. 选择目录: $ROOT/chrome_extension/"
  echo ""
  echo "微信小程序：微信开发者工具 → 导入 $ROOT/miniprogram/"
  echo ""
}

while true; do
  show_menu
  read -rp "请选择 [0-7]: " choice
  case "$choice" in
    1)
      python3 run_v8.py
      read -rp "按回车继续..."
      ;;
    2)
      echo "→ 启动 Streamlit 看板（Ctrl+C 停止）..."
      streamlit run dashboard/streamlit_app.py
      ;;
    3)
      echo "→ 启动 Web 服务（Ctrl+C 停止）..."
      echo "   打开 http://localhost:8080/web/"
      python3 -m http.server 8080
      ;;
    4)
      python3 mac_app/gui_app.py
      ;;
    5)
      python3 run_v8.py --all
      read -rp "按回车继续..."
      ;;
    6)
      python3 -m unittest tests.test_v7 tests.test_v8 -v
      read -rp "按回车继续..."
      ;;
    7)
      chrome_help
      read -rp "按回车继续..."
      ;;
    0)
      echo "再见 👋"
      exit 0
      ;;
    *)
      echo "无效选择"
      ;;
  esac
done
