"""Demo 组合状态 — v8 重平衡基准。"""

from __future__ import annotations

from typing import Any

DEFAULT_PORTFOLIO: dict[str, Any] = {
    "total_value": 100000.0,
    "cash_pct": 0.35,
    "holdings": {
        "588000": {"symbol": "科创50ETF", "pct": 0.35, "entry": 1.038},
        "510300": {"symbol": "沪深300ETF", "pct": 0.20, "entry": 3.86},
        "159915": {"symbol": "创业板ETF", "pct": 0.10, "entry": 2.18},
    },
}


def get_portfolio() -> dict[str, Any]:
    return DEFAULT_PORTFOLIO.copy()


def get_holding_pct(code: str) -> float:
    h = DEFAULT_PORTFOLIO["holdings"].get(code)
    return h["pct"] if h else 0.5
