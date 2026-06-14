"""v8 仓位重平衡 — 计算调仓路径。"""

from __future__ import annotations

from typing import Any


def rebalance_plan(
    code: str,
    symbol: str,
    price: float,
    target_pct: float,
    portfolio_value: float = 100000.0,
    current_pct: float = 0.5,
) -> dict[str, Any]:
    """生成组合重平衡计划。"""
    target_value = portfolio_value * target_pct
    current_value = portfolio_value * current_pct
    diff_value = target_value - current_value
    shares = int(abs(diff_value) / price / 100) * 100  # ETF 100 份整数倍

    if abs(diff_value) < portfolio_value * 0.02:
        action = "KEEP"
        action_label = "维持仓位"
    elif diff_value > 0:
        action = "INCREASE"
        action_label = "增持"
    else:
        action = "DECREASE"
        action_label = "减持"

    return {
        "code": code,
        "symbol": symbol,
        "price": price,
        "portfolio_value": portfolio_value,
        "current_pct": current_pct,
        "target_pct": target_pct,
        "current_value": round(current_value, 2),
        "target_value": round(target_value, 2),
        "diff_value": round(diff_value, 2),
        "shares": shares,
        "action": action,
        "action_label": action_label,
    }
