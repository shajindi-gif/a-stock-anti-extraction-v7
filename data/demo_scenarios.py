"""Demo 市场场景数据 — 模拟 Level2 盘口与资金流。"""

from __future__ import annotations

from typing import Any

DEMO_SCENARIOS: dict[str, dict[str, Any]] = {
    "bullish_kcb50": {
        "symbol": "科创50ETF",
        "code": "588000",
        "price": 1.052,
        "entry": 1.038,
        "volatility": 1.15,
        "spread_pct": 0.08,
        "volume_ratio": 1.2,
        "orderbook": {
            "bids": {1.051: 85000, 1.050: 120000, 1.049: 95000},
            "asks": {1.052: 42000, 1.053: 38000, 1.054: 51000},
        },
        "flow": {
            "direction": "inflow",
            "label": "资金流入中",
            "aggressive_buy": 156000,
            "aggressive_sell": 89000,
        },
        "sentiment": {
            "trap": "none",
            "trap_label": "无明显诱多",
        },
    },
    "sideways_hs300": {
        "symbol": "沪深300ETF",
        "code": "510300",
        "price": 3.856,
        "entry": 3.860,
        "volatility": 0.95,
        "spread_pct": 0.05,
        "volume_ratio": 0.85,
        "orderbook": {
            "bids": {3.855: 58000, 3.854: 55000, 3.853: 57000},
            "asks": {3.856: 62000, 3.857: 61000, 3.858: 64000},
        },
        "flow": {
            "direction": "inflow",
            "label": "资金小幅流入",
            "aggressive_buy": 65000,
            "aggressive_sell": 72000,
        },
        "sentiment": {
            "trap": "none",
            "trap_label": "无明显诱多",
        },
    },
    "bear_trap_detected": {
        "symbol": "创业板ETF",
        "code": "159915",
        "price": 2.145,
        "entry": 2.180,
        "volatility": 1.8,
        "spread_pct": 0.12,
        "volume_ratio": 0.55,
        "orderbook": {
            "bids": {2.144: 45000, 2.143: 38000, 2.142: 42000},
            "asks": {2.145: 88000, 2.146: 92000, 2.147: 76000},
        },
        "flow": {
            "direction": "outflow",
            "label": "资金流出",
            "aggressive_buy": 35000,
            "aggressive_sell": 98000,
        },
        "sentiment": {
            "trap": "bull_trap",
            "trap_label": "⚠️ 检测到诱多结构",
        },
    },
    "liquidity_crisis": {
        "symbol": "科创50ETF",
        "code": "588000",
        "price": 0.985,
        "entry": 1.020,
        "volatility": 2.5,
        "spread_pct": 0.65,
        "volume_ratio": 0.15,
        "orderbook": {
            "bids": {0.984: 8000, 0.983: 5000, 0.982: 3000},
            "asks": {0.985: 12000, 0.986: 9000, 0.987: 7000},
        },
        "flow": {
            "direction": "outflow",
            "label": "恐慌性流出",
            "aggressive_buy": 12000,
            "aggressive_sell": 85000,
        },
        "sentiment": {
            "trap": "panic_sell",
            "trap_label": "⚠️ 恐慌抛售结构",
        },
    },
}


def get_scenario(name: str) -> dict:
    """获取指定 demo 场景，默认返回 bullish_kcb50。"""
    return DEMO_SCENARIOS.get(name, DEMO_SCENARIOS["bullish_kcb50"]).copy()


def list_scenarios() -> list[str]:
    return list(DEMO_SCENARIOS.keys())
