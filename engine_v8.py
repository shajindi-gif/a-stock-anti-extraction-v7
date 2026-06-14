"""v8 引擎 — 在 v7 基础上叠加执行闭环与东方财富条件单。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from broker.eastmoney_conditional import build_conditional_orders, format_eastmoney_guide
from data.portfolio_state import get_holding_pct, get_portfolio
from engine import V7Result, run_v7_pipeline
from execution.auto_stop_executor import build_stop_plan
from execution.order_router import route_order
from execution.position_rebalancer import rebalance_plan


@dataclass
class V8Result:
    v7: V7Result
    order_route: dict[str, Any]
    rebalance: dict[str, Any]
    stop_plan: dict[str, Any]
    conditional_orders: list[dict[str, Any]] = field(default_factory=list)
    eastmoney_guide: str = ""

    def to_report(self) -> str:
        lines = [
            self.v7.to_report().replace(
                "🧠 A股反收割系统 v7（AI交易决策版）",
                "🚀 A股反收割系统 v8（自动交易闭环版）",
            ),
            "",
            "🔄 v8 执行闭环",
            "━━━━━━━━━━━━━━",
            f"📦 订单路由：{self.order_route['action_label']}（{self.order_route['intent']}）",
            f"  → {self.order_route['note']}",
            f"  → 建议份数：{self.order_route['lots'] * 100} 份",
            "━━━━━━━━━━━━━━",
            f"⚖️ 仓位重平衡：{self.rebalance['action_label']}",
            f"  → 当前 {self.rebalance['current_pct']:.0%} → 目标 {self.rebalance['target_pct']:.0%}",
            f"  → 调仓金额：{self.rebalance['diff_value']:+.0f} 元",
            f"  → 调仓份数：{self.rebalance['shares']} 份",
            "━━━━━━━━━━━━━━",
            f"🛡️ 自动止损：{self.stop_plan['status_label']}",
            f"  → 止损价 {self.stop_plan['stop_price']}（-{self.stop_plan['stop_pct']}%）",
            f"  → 止盈价 {self.stop_plan['take_profit_price']}（+{self.stop_plan['take_profit_pct']}%）",
            self.eastmoney_guide,
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        d = self.v7.to_dict()
        d.update({
            "version": "8.0.0",
            "order_route": self.order_route,
            "rebalance": self.rebalance,
            "stop_plan": self.stop_plan,
            "conditional_orders": self.conditional_orders,
            "eastmoney_guide": self.eastmoney_guide,
        })
        return d


def run_v8_pipeline(
    scenario: dict[str, Any],
    portfolio_value: float | None = None,
    current_holding_pct: float | None = None,
) -> V8Result:
    """执行 v8 完整流水线（v7 决策 + 执行闭环 + 东财条件单）。"""
    v7 = run_v7_pipeline(scenario)
    portfolio = get_portfolio()
    pv = portfolio_value or portfolio["total_value"]
    holding = current_holding_pct if current_holding_pct is not None else get_holding_pct(v7.code)

    order_route = route_order(v7.decision, v7.position, holding)
    rebalance = rebalance_plan(
        v7.code, v7.symbol, v7.price, v7.position, pv, holding,
    )
    stop_plan = build_stop_plan(
        v7.price, scenario["entry"], v7.stop_pct, v7.decision, scenario["volatility"],
    )
    conditional_orders = build_conditional_orders(
        v7.code, v7.symbol, v7.price, v7.decision,
        order_route, stop_plan, rebalance,
    )
    eastmoney_guide = format_eastmoney_guide(conditional_orders)

    return V8Result(
        v7=v7,
        order_route=order_route,
        rebalance=rebalance,
        stop_plan=stop_plan,
        conditional_orders=conditional_orders,
        eastmoney_guide=eastmoney_guide,
    )


def run_all_scenarios_v8() -> list[dict[str, Any]]:
    """批量运行全部 Demo 场景，供看板使用。"""
    from data.demo_scenarios import get_scenario, list_scenarios

    rows = []
    for name in list_scenarios():
        r = run_v8_pipeline(get_scenario(name))
        rows.append({
            "scenario": name,
            "symbol": r.v7.symbol,
            "code": r.v7.code,
            "price": r.v7.price,
            "decision": r.v7.decision,
            "position": r.v7.position,
            "prob_up": r.v7.probability["up"],
            "prob_side": r.v7.probability["side"],
            "prob_down": r.v7.probability["down"],
            "regime": r.v7.regime_label,
            "order_intent": r.order_route["intent"],
            "rebalance_action": r.rebalance["action_label"],
            "stop_status": r.stop_plan["status_label"],
            "conditional_count": len(r.conditional_orders),
        })
    return rows
