"""v8 订单路由 — 将 AI 决策映射为可执行订单意图（模拟/纸面）。"""

from __future__ import annotations

from typing import Any, Literal

OrderIntent = Literal["BUY", "SELL", "HOLD", "NO_ACTION"]


def route_order(
    decision: str,
    position: float,
    current_holding_pct: float = 0.5,
) -> dict[str, Any]:
    """根据 AI 决策与目标仓位生成订单路由意图。"""
    delta = round(position - current_holding_pct, 2)

    if decision == "NO_TRADE":
        return {
            "intent": "NO_ACTION",
            "action_label": "禁止交易",
            "target_position": position,
            "current_position": current_holding_pct,
            "delta": 0.0,
            "lots": 0,
            "note": "流动性危机，暂停一切下单",
        }

    if decision == "BUY_TREND" and delta > 0.05:
        lots = max(1, int(delta * 100))
        return {
            "intent": "BUY",
            "action_label": "加仓买入",
            "target_position": position,
            "current_position": current_holding_pct,
            "delta": delta,
            "lots": lots,
            "note": f"趋势跟随，目标仓位 {position:.0%}，需增仓 {delta:.0%}",
        }

    if decision in ("REDUCE_POSITION",) or (decision == "HOLD" and delta < -0.05):
        lots = max(1, int(abs(delta) * 100)) if delta < 0 else max(1, int(position * 30))
        return {
            "intent": "SELL",
            "action_label": "减仓卖出",
            "target_position": position,
            "current_position": current_holding_pct,
            "delta": delta,
            "lots": lots,
            "note": "风险升高，建议减仓",
        }

    if decision == "MEAN_REVERSION":
        return {
            "intent": "HOLD",
            "action_label": "震荡观望",
            "target_position": position,
            "current_position": current_holding_pct,
            "delta": delta,
            "lots": 0,
            "note": "震荡结构，等待区间边界触发条件单",
        }

    return {
        "intent": "HOLD",
        "action_label": "持有观望",
        "target_position": position,
        "current_position": current_holding_pct,
        "delta": delta,
        "lots": 0,
        "note": "仓位接近目标，暂不操作",
    }
