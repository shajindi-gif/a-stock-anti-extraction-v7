"""v8 模块单元测试。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from broker.eastmoney_conditional import build_conditional_orders, format_eastmoney_guide
from data.demo_scenarios import get_scenario, list_scenarios
from engine_v8 import run_all_scenarios_v8, run_v8_pipeline
from execution.auto_stop_executor import build_stop_plan
from execution.order_router import route_order
from execution.position_rebalancer import rebalance_plan


class TestV8(unittest.TestCase):
    def test_order_router_buy(self):
        r = route_order("BUY_TREND", 0.7, 0.3)
        self.assertEqual(r["intent"], "BUY")
        self.assertGreater(r["lots"], 0)

    def test_order_router_no_trade(self):
        r = route_order("NO_TRADE", 0.7, 0.5)
        self.assertEqual(r["intent"], "NO_ACTION")

    def test_rebalance_plan(self):
        p = rebalance_plan("588000", "科创50ETF", 1.05, 0.7, 100000, 0.3)
        self.assertEqual(p["action"], "INCREASE")
        self.assertGreater(p["shares"], 0)

    def test_stop_plan(self):
        s = build_stop_plan(1.05, 1.0, 2.3, "BUY_TREND", 1.15)
        self.assertEqual(s["status"], "ARMED")
        self.assertLess(s["stop_price"], 1.0)

    def test_eastmoney_conditional_orders(self):
        scenario = get_scenario("bullish_kcb50")
        result = run_v8_pipeline(scenario)
        self.assertGreater(len(result.conditional_orders), 0)
        guide = format_eastmoney_guide(result.conditional_orders)
        self.assertIn("东方财富", guide)

    def test_v8_pipeline_all_scenarios(self):
        for name in list_scenarios():
            r = run_v8_pipeline(get_scenario(name))
            self.assertIsNotNone(r.v7.decision)
            self.assertIn("intent", r.order_route)
            self.assertIn("version", r.to_dict())

    def test_liquidity_crisis_no_orders_or_disabled(self):
        r = run_v8_pipeline(get_scenario("liquidity_crisis"))
        self.assertEqual(r.v7.decision, "NO_TRADE")
        self.assertEqual(r.order_route["intent"], "NO_ACTION")
        self.assertEqual(r.stop_plan["status"], "DISABLED")

    def test_run_all_scenarios_v8(self):
        rows = run_all_scenarios_v8()
        self.assertEqual(len(rows), len(list_scenarios()))

    def test_v8_report_contains_v8_sections(self):
        report = run_v8_pipeline(get_scenario("bullish_kcb50")).to_report()
        self.assertIn("v8", report)
        self.assertIn("东方财富条件单", report)
        self.assertIn("执行闭环", report)


if __name__ == "__main__":
    unittest.main()
