# 🚀 A股反收割系统 v7

**AI交易决策系统（Level2 + 预测版）**

从 v6 的「盘口识别」升级为 **盘口 + 资金 + 情绪 → 下一步走势概率预测**，形成完整的 AI 交易决策流水线。

> ⚠️ **免责声明**：本系统为结构概率决策工具，用于研究与学习，不构成任何投资建议。不保证盈利。

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
├── engine.py            # 核心流水线
└── run_v7.py            # 主入口
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

# 默认场景（科创50ETF 多头结构）
python3 run_v7.py

# 指定场景
python3 run_v7.py -s bear_trap_detected

# JSON 输出
python3 run_v7.py --json

# 列出所有场景
python3 run_v7.py --list
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
python3 -m unittest tests.test_v7 -v
```

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

## 🔮 v8 展望

- 券商 API 自动下单
- 自动调仓与止损
- 多策略组合运行

## 📄 License

MIT
