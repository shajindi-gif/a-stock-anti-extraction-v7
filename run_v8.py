#!/usr/bin/env python3
"""A股反收割系统 v8 — 自动交易闭环入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.demo_scenarios import get_scenario, list_scenarios  # noqa: E402
from engine_v8 import run_all_scenarios_v8, run_v8_pipeline  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A股反收割系统 v8 | 自动交易闭环 + 东方财富条件单",
    )
    parser.add_argument(
        "--scenario", "-s",
        default="bullish_kcb50",
        choices=list_scenarios(),
        help="Demo 场景名称",
    )
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--list", action="store_true", help="列出场景")
    parser.add_argument("--all", action="store_true", help="运行全部场景摘要")
    args = parser.parse_args()

    if args.list:
        print("可用 Demo 场景：")
        for name in list_scenarios():
            s = get_scenario(name)
            print(f"  • {name:25s} → {s['symbol']} ({s['code']})")
        return 0

    if args.all:
        rows = run_all_scenarios_v8()
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            print("\n🚀 v8 全场景执行摘要\n" + "─" * 60)
            for r in rows:
                print(
                    f"{r['symbol']:12s} | {r['decision']:16s} | "
                    f"仓位 {r['position']:.0%} | 条件单 {r['conditional_count']} 条 | "
                    f"{r['rebalance_action']}"
                )
        return 0

    result = run_v8_pipeline(get_scenario(args.scenario))
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.to_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
