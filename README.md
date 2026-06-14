# 🚀 A股反收割系统 v7 → v8

**v7**：AI交易决策（Level2 + 预测版）  
**v8**：自动交易闭环 + 东方财富条件单 + Streamlit 数据看板

> ⚠️ **免责声明**：本系统为结构概率决策工具，用于研究与学习，不构成任何投资建议。v8 不自动下单，条件单需在东财 APP 手动设置。

---

## 🧠 系统架构

```
a_stock_anti_extraction_v7/
├── prediction/          # 方向预测 + 概率引擎
│   ├── next_move_model.py
│   └── probability_engine.py
├── decision/            # AI 交易员 + 动态仓位
│   ├── ai_trader.py
│   └── position_adaptor.py
├── risk/                # 动态止损 + 市场状态保护
│   ├── dynamic_stop.py
│   └── regime_guard.py
├── signal/              # 多信号融合
│   └── fused_signal.py
├── data/                # Demo 场景数据
├── demo/                # 交互式 CLI Demo
├── mac_app/             # macOS 桌面应用
├── web/                 # Web 网页版 Demo
├── chrome_extension/    # Google Chrome 浏览器插件
├── miniprogram/         # 微信小程序
├── shared/js/           # 跨平台 JS 核心（v7-core + v8-core）
├── execution/           # v8 订单路由 / 重平衡 / 自动止损
├── broker/              # v8 东方财富条件单建议
├── dashboard/           # v8 Streamlit 数据看板
├── engine.py            # v7 Python 流水线
├── engine_v8.py         # v8 Python 流水线（叠加执行闭环）
├── run_v7.py            # v7 入口（make run）
└── run_v8.py            # v8 入口（make run-v8）
```

## 🔄 决策流水线

```
Level2盘口 + 资金流 + 情绪信号
        ↓
   多信号融合 (fused_signal)
        ↓
   方向预测 (next_move_model)
        ↓
   概率计算 (probability_engine)
        ↓
   市场状态检测 (regime_guard)
        ↓
   AI 决策 (ai_trader) + 动态仓位 (position_adaptor)
        ↓
   动态止损 (dynamic_stop)
        ↓
   完整交易报告
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- macOS 11+（桌面应用）
- 无第三方依赖（标准库即可运行）

### CLI 运行

```bash
cd a_stock_anti_extraction_v7

# v7 默认场景（make run 不变）
python3 run_v7.py
make run

# v8 自动交易闭环 + 东财条件单
python3 run_v8.py
make run-v8

# v8 全场景摘要
python3 run_v8.py --all

# 指定场景 / JSON
python3 run_v8.py -s bear_trap_detected --json
```

### Demo

```bash
# 运行全部 4 个场景
python3 demo/demo_cli.py --all

# 交互式选择
python3 demo/demo_cli.py
```

### macOS 桌面应用

```bash
# 直接启动 GUI
python3 mac_app/gui_app.py

# 或使用 Make
make gui

# 构建 .app 应用包
make build-app
open dist/A股反收割系统v7.app
```

### 测试

```bash
make test
# 或
python3 -m unittest tests.test_v7 tests.test_v8 -v
```

### v8 Streamlit 数据看板

```bash
pip install streamlit pandas
make dashboard
```

详见 [dashboard/README.md](dashboard/README.md)

看板包含：决策概览、执行闭环、东方财富条件单、全场景对比四个 Tab。

### Web 网页版

```bash
# 启动本地服务器
./scripts/serve_web.sh
# 浏览器打开 http://localhost:8080/web/
```

也可将 `web/` 目录部署到 GitHub Pages / 任意静态托管。

### Chrome 浏览器插件

```bash
# 生成图标（首次）
python3 scripts/generate_icons.py

# Chrome 打开 chrome://extensions/ → 开发者模式 → 加载已解压的扩展
# 选择 chrome_extension/ 目录
```

详见 [chrome_extension/README.md](chrome_extension/README.md)

### 微信小程序

1. 用微信开发者工具导入 `miniprogram/` 目录
2. AppID 可选测试号
3. 编译预览即可

详见 [miniprogram/README.md](miniprogram/README.md)

### 同步 JS 核心到各端

修改 `shared/js/v7-core.js` 或 `v8-core.js` 后运行：

```bash
./scripts/sync_js.sh
```

Web / Chrome / 小程序均已集成 v8 执行闭环与东财条件单展示。

## 📊 Demo 场景

| 场景 | 标的 | 预期决策 |
|------|------|----------|
| `bullish_kcb50` | 科创50ETF | BUY_TREND |
| `sideways_hs300` | 沪深300ETF | HOLD（震荡概率 50%） |
| `bear_trap_detected` | 创业板ETF | HOLD（下跌概率 50%） |
| `liquidity_crisis` | 科创50ETF | NO_TRADE |

## 📋 示例输出

```
🧠 A股反收割系统 v7（AI交易决策版）
━━━━━━━━━━━━━━
📊 标的：科创50ETF (588000)
💹 当前价：1.052
🧠 预测结果：
  - 上涨概率：70%
  - 震荡概率：20%
  - 下跌风险：10%
━━━━━━━━━━━━━━
📉 AI决策：
  👉 BUY_TREND（趋势跟随）
━━━━━━━━━━━━━━
💰 仓位建议：
  → 70%
━━━━━━━━━━━━━━
⚠️ 风险控制：
  → 市场状态：正常
  → 动态止损 -2.3%
  → 止损状态：HOLD
━━━━━━━━━━━━━━
🧨 结构判断：
  → 无明显诱多
  → 资金流入中
  → 盘口强度比 2.02
━━━━━━━━━━━━━━
```

## 🧩 v7 三大核心能力

1. **盘口 → 概率化预测** — 将 Level2 结构转化为 UP/SIDE/DOWN 概率
2. **多信号融合 → 交易决策** — AI 交易员综合概率与市场状态
3. **动态仓位控制** — 根据概率分布自动调整建议仓位（10%~80%）

## 📈 版本演进

| 版本 | 能力 |
|------|------|
| v1 | 识别收割 |
| v2 | 日报 |
| v3 | 分时 |
| v4 | 盘口结构 |
| v5 | 资金流 |
| v6 | 订单流 |
| **v7** | **AI 预测 + 决策** |
| **v8** | **执行闭环 + 东财条件单 + 数据看板** |

## 🚀 v8 核心能力

1. **订单路由** — AI 决策 → 买/卖/持有/禁止
2. **仓位重平衡** — 目标仓位 vs 当前持仓，计算调仓份数
3. **自动止损计划** — 动态止损价 / 止盈价 / 触发状态
4. **东方财富条件单** — 止损/止盈/定价买卖/回落卖出，含 APP 操作路径
5. **Streamlit 看板** — 全场景对比、概率图表、条件单一览

## 🔮 v9 展望

- 券商 API 真实自动下单
- 多策略组合并行
- 实时行情接入

## 📄 License

MIT
