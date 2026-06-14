"""结构概率引擎 — 将方向信号转化为概率分布。"""

from __future__ import annotations

from typing import Literal, TypedDict

from .next_move_model import Signal


class Probability(TypedDict):
    up: float
    side: float
    down: float


def calc_probability(signal: Signal) -> Probability:
    """根据预测信号计算上涨/震荡/下跌概率。"""
    if signal == "UP_PROB_HIGH":
        return {"up": 0.7, "side": 0.2, "down": 0.1}
    if signal == "SIDEWAYS":
        return {"up": 0.3, "side": 0.5, "down": 0.2}
    return {"up": 0.2, "side": 0.3, "down": 0.5}
