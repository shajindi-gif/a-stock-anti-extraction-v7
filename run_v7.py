#!/usr/bin/env python3
"""A股反收割系统 v7 — 主入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.demo_scenarios import get_scenario, list_scenarios  # noqa: E402
from engine import run_v7_pipeline  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A股反收割系统 v7 | AI交易决策系统（Level2+预测版）",
    )
    parser.add_argument(
        "--scenario",
        "-s",
        default="bullish_kcb50",
        choices=list_scenarios(),
        help="Demo 场景名称",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出结果",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用 demo 场景",
    )
    args = parser.parse_args()

    if args.list:
        print("可用 Demo 场景：")
        for name in list_scenarios():
            s = get_scenario(name)
            print(f"  • {name:25s} → {s['symbol']} ({s['code']})")
        return 0

    scenario = get_scenario(args.scenario)
    result = run_v7_pipeline(scenario)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.to_report())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
