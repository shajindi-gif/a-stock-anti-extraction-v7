# 🚀 A股反收割系统 v8

[![CI](https://github.com/shajindi-gif/a-stock-anti-extraction-v7/actions/workflows/ci.yml/badge.svg)](https://github.com/shajindi-gif/a-stock-anti-extraction-v7/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)

**任何人都能用的 A 股 AI 交易决策演示产品**

- 🧠 AI 预测：盘口 + 资金 + 情绪 → 上涨/震荡/下跌概率
- 🔄 执行闭环：订单路由、仓位重平衡、自动止损计划
- 📱 东方财富条件单：可直接复制到东财 APP 设置
- 🖥️ **6 种使用方式**：终端 / 看板 / 网页 / Mac / Chrome / 微信小程序

> ⚠️ **免责声明**：结构概率演示工具，不构成投资建议，不自动下单。

**📖 新手请读：[QUICKSTART.md](QUICKSTART.md)（3 分钟上手）**

**🌐 在线体验（无需安装）：** https://shajindi-gif.github.io/a-stock-anti-extraction-v7/

---

## ⚡ 一键开始

```bash
git clone https://github.com/shajindi-gif/a-stock-anti-extraction-v7.git
cd a-stock-anti-extraction-v7
make install          # 安装依赖 + 测试
make start            # 交互式菜单（推荐）
```

或直接：

```bash
make run-v8           # 终端完整报告
make dashboard        # Streamlit 数据看板
make web              # 本地网页 → http://localhost:8080/web/
make gui              # Mac 图形界面
```

---

## 📦 全部产品形态

| 产品 | 命令 / 方式 | 说明 |
|------|-------------|------|
| **交互菜单** | `make start` | 一个菜单启动所有功能 |
| **v8 终端** | `make run-v8` | 完整报告 + 东财条件单 |
| **Streamlit 看板** | `make dashboard` | 4 Tab 可视化数据看板 |
| **Web 网页** | [在线](https://shajindi-gif.github.io/a-stock-anti-extraction-v7/) 或 `make web` | 浏览器即用 |
| **Mac 桌面** | `make gui` / `make build-app` | tkinter GUI / .app |
| **Chrome 插件** | `make chrome` → 加载 `chrome_extension/` | 弹窗 + 行情页浮标 |
| **微信小程序** | 微信开发者工具导入 `miniprogram/` | 手机预览 |
| **v7 终端** | `make run` | 仅 AI 决策（兼容保留） |

---

## 🧠 系统架构

```
a_stock_anti_extraction_v7/
├── prediction/ decision/ risk/ signal/   # v7 AI 决策核心
├── execution/ broker/                     # v8 执行 + 东财条件单
├── dashboard/streamlit_app.py             # 数据看板
├── web/ chrome_extension/ miniprogram/    # 三端产品
├── mac_app/gui_app.py                     # Mac 桌面
├── shared/js/v7-core.js + v8-core.js      # 跨端 JS 引擎
├── scripts/install.sh + start.sh          # 一键安装 / 启动
├── engine_v8.py + run_v8.py               # v8 主入口
└── tests/                                 # 20 项自动化测试
```

---

## 📊 Demo 场景

| 场景 | 标的 | 典型结果 |
|------|------|----------|
| `bullish_kcb50` | 科创50ETF | BUY_TREND + 买入条件单 |
| `sideways_hs300` | 沪深300ETF | HOLD + 观望 |
| `bear_trap_detected` | 创业板ETF | 诱多预警 + 减仓 |
| `liquidity_crisis` | 科创50ETF | NO_TRADE 禁止交易 |

```bash
python3 run_v8.py -s bear_trap_detected   # 切换场景
python3 run_v8.py --all                   # 4 场景一览
```

---

## 🛠 开发 & 测试

```bash
make test              # 20 项测试
make sync-js           # 同步 JS 到 web/chrome/小程序
make clean             # 清理缓存
```

---

## 📈 版本演进

| 版本 | 能力 |
|------|------|
| v1–v6 | 识别 → 日报 → 分时 → 盘口 → 资金 → 订单流 |
| **v7** | AI 预测 + 决策 |
| **v8** | 执行闭环 + 东财条件单 + 6 端产品 + 数据看板 |

---

## 📄 License

MIT · [shajindi-gif](https://github.com/shajindi-gif)
