"""动态仓位适配器 — 根据概率分布调整建议仓位。"""

from __future__ import annotations

from prediction.probability_engine import Probability


def adapt_position(prob: Probability) -> float:
    """根据上涨概率动态调整目标仓位（0.1 ~ 0.8）。"""
    base = 0.5
    base += prob["up"] - 0.5
    if base > 0.8:
        return 0.8
    if base < 0.1:
        return 0.1
    return round(base, 2)
