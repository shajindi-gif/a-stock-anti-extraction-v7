"""下一分钟/下一小时方向预测模型。"""

from __future__ import annotations

from typing import Literal, TypedDict


Signal = Literal["UP_PROB_HIGH", "SIDEWAYS", "DOWN_RISK"]


class MarketSnapshot(TypedDict):
    bid_strength: float
    ask_strength: float
    flow: str
    aggressive_buy: float
    aggressive_sell: float
    trap: str


def predict_next_move(market: MarketSnapshot) -> Signal:
    """基于盘口、资金流、成交结构与诱多识别，预测下一步走势方向。"""
    score = 0

    if market["bid_strength"] > market["ask_strength"]:
        score += 1

    if market["flow"] == "inflow":
        score += 1

    if market["aggressive_buy"] > market["aggressive_sell"]:
        score += 1

    if market["trap"] == "none":
        score += 1
    else:
        score -= 2

    if score >= 3:
        return "UP_PROB_HIGH"
    if score == 2:
        return "SIDEWAYS"
    return "DOWN_RISK"
