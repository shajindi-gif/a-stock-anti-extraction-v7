#!/usr/bin/env python3
"""交互式 Demo — 演示 v7 全部场景。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.demo_scenarios import get_scenario, list_scenarios  # noqa: E402
from engine import run_v7_pipeline  # noqa: E402

SCENARIO_DESC = {
    "bullish_kcb50": "科创50ETF 多头结构 — 典型 BUY_TREND 场景",
    "sideways_hs300": "沪深300ETF 震荡结构 — SIDEWAYS / HOLD 场景",
    "bear_trap_detected": "创业板ETF 诱多结构 — DOWN_RISK 场景",
    "liquidity_crisis": "科创50ETF 流动性危机 — NO_TRADE 场景",
}


def run_all_demos() -> None:
    print("=" * 60)
    print("  🚀 A股反收割系统 v7 — 全场景 Demo")
    print("=" * 60)

    for i, name in enumerate(list_scenarios(), 1):
        print(f"\n【场景 {i}/{len(list_scenarios())}】{SCENARIO_DESC.get(name, name)}")
        print("-" * 60)
        result = run_v7_pipeline(get_scenario(name))
        print(result.to_report())


def run_interactive() -> None:
    print("\n🧠 A股反收割系统 v7 — 交互式 Demo\n")
    scenarios = list_scenarios()
    for i, name in enumerate(scenarios, 1):
        desc = SCENARIO_DESC.get(name, name)
        print(f"  {i}. {name} — {desc}")

    while True:
        try:
            choice = input("\n选择场景编号 (1-4) 或 q 退出: ").strip()
            if choice.lower() in ("q", "quit", "exit"):
                print("再见 👋")
                break
            idx = int(choice) - 1
            if 0 <= idx < len(scenarios):
                result = run_v7_pipeline(get_scenario(scenarios[idx]))
                print(result.to_report())
            else:
                print("无效选择，请重试。")
        except (ValueError, KeyboardInterrupt):
            print("\n再见 👋")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all_demos()
    else:
        run_interactive()
