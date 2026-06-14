"""东方财富条件单建议 — 根据 v8 决策生成 APP 可操作的条件单参数。"""

from __future__ import annotations

from typing import Any


def build_conditional_orders(
    code: str,
    symbol: str,
    price: float,
    decision: str,
    order_route: dict[str, Any],
    stop_plan: dict[str, Any],
    rebalance: dict[str, Any],
) -> list[dict[str, Any]]:
    """生成东方财富条件单建议列表。"""
    orders: list[dict[str, Any]] = []

    # 1. 止损条件单（始终建议布防，除非 NO_TRADE）
    if decision != "NO_TRADE":
        orders.append({
            "type": "止损卖出",
            "type_code": "stop_loss",
            "code": code,
            "symbol": symbol,
            "trigger_price": stop_plan["stop_price"],
            "order_price": "市价",
            "quantity": f"{rebalance['shares'] or 100} 份",
            "valid_days": "30天",
            "priority": "高",
            "reason": f"动态止损 -{stop_plan['stop_pct']}%，保护本金",
            "app_path": "东方财富 APP → 交易 → 条件单 → 止损",
        })

    # 2. 止盈条件单
    if decision in ("BUY_TREND", "MEAN_REVERSION", "HOLD") and decision != "NO_TRADE":
        orders.append({
            "type": "止盈卖出",
            "type_code": "take_profit",
            "code": code,
            "symbol": symbol,
            "trigger_price": stop_plan["take_profit_price"],
            "order_price": "限价",
            "quantity": f"{max(rebalance['shares'] // 2, 100)} 份",
            "valid_days": "60天",
            "priority": "中",
            "reason": f"目标止盈 +{stop_plan['take_profit_pct']}%",
            "app_path": "东方财富 APP → 交易 → 条件单 → 止盈",
        })

    # 3. 定价买入（趋势跟随）
    if order_route["intent"] == "BUY":
        buy_trigger = round(price * 0.998, 3)
        orders.append({
            "type": "定价买入",
            "type_code": "limit_buy",
            "code": code,
            "symbol": symbol,
            "trigger_price": buy_trigger,
            "order_price": str(buy_trigger),
            "quantity": f"{order_route['lots'] * 100} 份",
            "valid_days": "5天",
            "priority": "高",
            "reason": order_route["note"],
            "app_path": "东方财富 APP → 交易 → 条件单 → 定价买入",
        })

    # 4. 定价卖出（减仓）
    if order_route["intent"] == "SELL":
        sell_trigger = round(price * 1.002, 3)
        orders.append({
            "type": "定价卖出",
            "type_code": "limit_sell",
            "code": code,
            "symbol": symbol,
            "trigger_price": sell_trigger,
            "order_price": "市价",
            "quantity": f"{order_route['lots'] * 100} 份",
            "valid_days": "5天",
            "priority": "高",
            "reason": order_route["note"],
            "app_path": "东方财富 APP → 交易 → 条件单 → 定价卖出",
        })

    # 5. 回落卖出（诱多保护）
    if decision in ("HOLD", "REDUCE_POSITION"):
        orders.append({
            "type": "回落卖出",
            "type_code": "trailing_sell",
            "code": code,
            "symbol": symbol,
            "trigger_price": round(price * 0.99, 3),
            "order_price": "市价",
            "quantity": f"{max(rebalance['shares'] // 2, 100)} 份",
            "valid_days": "10天",
            "priority": "中",
            "reason": "从近期高点回落 1% 自动减仓",
            "app_path": "东方财富 APP → 交易 → 条件单 → 回落卖出",
        })

    return orders


def format_eastmoney_guide(orders: list[dict[str, Any]]) -> str:
    """格式化东方财富条件单操作指南。"""
    if not orders:
        return "当前无需设置条件单。"

    lines = [
        "",
        "📱 东方财富条件单建议",
        "━━━━━━━━━━━━━━",
    ]
    for i, o in enumerate(orders, 1):
        lines.extend([
            f"【条件单 {i}】{o['type']}（优先级：{o['priority']}）",
            f"  标的：{o['symbol']} ({o['code']})",
            f"  触发价：{o['trigger_price']}",
            f"  委托价：{o['order_price']}",
            f"  数量：{o['quantity']}",
            f"  有效期：{o['valid_days']}",
            f"  理由：{o['reason']}",
            f"  操作路径：{o['app_path']}",
            "",
        ])
    lines.extend([
        "━━━━━━━━━━━━━━",
        "💡 提示：请在东方财富 APP 手动设置，本系统不自动下单。",
    ])
    return "\n".join(lines)
