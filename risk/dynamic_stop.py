"""动态止损模块。"""

from __future__ import annotations

from typing import Literal

StopAction = Literal["STOP_OUT", "HOLD"]


def calc_stop_pct(volatility: float) -> float:
    """计算动态止损百分比。"""
    return round(0.02 * volatility * 100, 1)


def stop_loss(price: float, entry: float, volatility: float) -> StopAction:
    """判断是否触发动态止损。"""
    if price < entry * (1 - 0.02 * volatility):
        return "STOP_OUT"
    return "HOLD"
