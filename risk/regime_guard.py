"""市场状态保护 — 识别流动性危机等极端状态。"""

from __future__ import annotations

from typing import Literal

Regime = Literal["NORMAL", "HIGH_VOLATILITY", "LIQUIDITY_CRISIS"]

REGIME_LABELS = {
    "NORMAL": "正常",
    "HIGH_VOLATILITY": "高波动",
    "LIQUIDITY_CRISIS": "流动性危机",
}


def detect_regime(
    volatility: float,
    spread_pct: float,
    volume_ratio: float,
) -> Regime:
    """根据波动率、买卖价差与成交量比检测市场状态。"""
    if spread_pct > 0.5 or volume_ratio < 0.3:
        return "LIQUIDITY_CRISIS"
    if volatility > 1.5:
        return "HIGH_VOLATILITY"
    return "NORMAL"
