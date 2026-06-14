"""多信号融合 — 将盘口、资金、情绪信号合成为市场快照。"""

from __future__ import annotations

from typing import Any

from prediction.next_move_model import MarketSnapshot


def fuse_signals(
    orderbook: dict[str, float],
    flow: dict[str, Any],
    sentiment: dict[str, Any],
) -> dict[str, Any]:
    """融合盘口、资金流与情绪信号。"""
    bid_total = sum(orderbook.get("bids", {}).values())
    ask_total = sum(orderbook.get("asks", {}).values())

    return {
        "bid_strength": bid_total,
        "ask_strength": ask_total,
        "flow": flow.get("direction", "neutral"),
        "aggressive_buy": flow.get("aggressive_buy", 0),
        "aggressive_sell": flow.get("aggressive_sell", 0),
        "trap": sentiment.get("trap", "none"),
        "flow_label": flow.get("label", "中性"),
        "trap_label": sentiment.get("trap_label", "无明显诱多"),
    }


def build_market_snapshot(fused: dict[str, Any]) -> MarketSnapshot:
    """将融合信号转换为预测模型所需的市场快照。"""
    return MarketSnapshot(
        bid_strength=fused["bid_strength"],
        ask_strength=fused["ask_strength"],
        flow=fused["flow"],
        aggressive_buy=fused["aggressive_buy"],
        aggressive_sell=fused["aggressive_sell"],
        trap=fused["trap"],
    )
