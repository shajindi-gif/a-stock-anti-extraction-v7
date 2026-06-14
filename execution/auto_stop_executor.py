"""v8 自动止损执行计划。"""

from __future__ import annotations

from typing import Any


def build_stop_plan(
    price: float,
    entry: float,
    stop_pct: float,
    decision: str,
    volatility: float,
) -> dict[str, Any]:
    """生成止损 / 止盈执行计划。"""
    stop_price = round(entry * (1 - stop_pct / 100), 3)
    take_profit_pct = round(stop_pct * 2, 1)
    take_profit_price = round(entry * (1 + take_profit_pct / 100), 3)
    trailing_pct = round(stop_pct * 0.8, 1)

    triggered = price < stop_price
    status = "TRIGGERED" if triggered else "ARMED"

    if decision == "NO_TRADE":
        status = "DISABLED"

    return {
        "entry": entry,
        "current_price": price,
        "stop_pct": stop_pct,
        "stop_price": stop_price,
        "take_profit_pct": take_profit_pct,
        "take_profit_price": take_profit_price,
        "trailing_stop_pct": trailing_pct,
        "status": status,
        "status_label": {
            "TRIGGERED": "已触发止损",
            "ARMED": "止损已布防",
            "DISABLED": "止损已禁用",
        }.get(status, status),
        "volatility": volatility,
    }
