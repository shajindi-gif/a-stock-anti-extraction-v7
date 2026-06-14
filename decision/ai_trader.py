"""AI 交易员 — 基于概率与市场状态做出交易决策。"""

from __future__ import annotations

from typing import Literal

from prediction.probability_engine import Probability

Decision = Literal[
    "NO_TRADE",
    "BUY_TREND",
    "REDUCE_POSITION",
    "MEAN_REVERSION",
    "HOLD",
]

DECISION_LABELS = {
    "NO_TRADE": "禁止交易（流动性危机）",
    "BUY_TREND": "趋势跟随",
    "REDUCE_POSITION": "减仓避险",
    "MEAN_REVERSION": "均值回归",
    "HOLD": "观望持有",
}


def ai_decision(prob: Probability, regime: str) -> Decision:
    """根据概率分布与市场状态生成 AI 交易决策。"""
    if regime == "LIQUIDITY_CRISIS":
        return "NO_TRADE"
    if prob["up"] > 0.65:
        return "BUY_TREND"
    if prob["down"] > 0.6:
        return "REDUCE_POSITION"
    if prob["side"] > 0.5:
        return "MEAN_REVERSION"
    return "HOLD"
