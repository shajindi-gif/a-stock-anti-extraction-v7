"""v7 核心模块单元测试（标准库 unittest，无第三方依赖）。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.demo_scenarios import get_scenario, list_scenarios
from decision.ai_trader import ai_decision
from decision.position_adaptor import adapt_position
from engine import run_v7_pipeline
from prediction.next_move_model import predict_next_move
from prediction.probability_engine import calc_probability
from risk.dynamic_stop import calc_stop_pct, stop_loss
from risk.regime_guard import detect_regime
from signal.fused_signal import build_market_snapshot, fuse_signals


class TestV7(unittest.TestCase):
    def test_predict_next_move_bullish(self):
        market = build_market_snapshot(
            fuse_signals(
                {"bids": {1.0: 100}, "asks": {1.0: 50}},
                {"direction": "inflow", "aggressive_buy": 80, "aggressive_sell": 40},
                {"trap": "none"},
            )
        )
        self.assertEqual(predict_next_move(market), "UP_PROB_HIGH")

    def test_predict_next_move_trap(self):
        market = build_market_snapshot(
            fuse_signals(
                {"bids": {1.0: 100}, "asks": {1.0: 50}},
                {"direction": "inflow", "aggressive_buy": 80, "aggressive_sell": 40},
                {"trap": "bull_trap"},
            )
        )
        self.assertEqual(predict_next_move(market), "DOWN_RISK")

    def test_calc_probability(self):
        prob = calc_probability("UP_PROB_HIGH")
        self.assertEqual(prob["up"], 0.7)
        self.assertAlmostEqual(prob["up"] + prob["side"] + prob["down"], 1.0)

    def test_ai_decision_buy(self):
        prob = {"up": 0.7, "side": 0.2, "down": 0.1}
        self.assertEqual(ai_decision(prob, "NORMAL"), "BUY_TREND")

    def test_ai_decision_no_trade(self):
        prob = {"up": 0.7, "side": 0.2, "down": 0.1}
        self.assertEqual(ai_decision(prob, "LIQUIDITY_CRISIS"), "NO_TRADE")

    def test_adapt_position(self):
        self.assertEqual(adapt_position({"up": 0.7, "side": 0.2, "down": 0.1}), 0.7)

    def test_dynamic_stop(self):
        self.assertEqual(stop_loss(0.95, 1.0, 1.0), "STOP_OUT")
        self.assertEqual(stop_loss(0.99, 1.0, 1.0), "HOLD")
        self.assertEqual(calc_stop_pct(1.15), 2.3)

    def test_regime_guard(self):
        self.assertEqual(detect_regime(1.0, 0.05, 1.0), "NORMAL")
        self.assertEqual(detect_regime(2.0, 0.05, 1.0), "HIGH_VOLATILITY")
        self.assertEqual(detect_regime(1.0, 0.6, 0.2), "LIQUIDITY_CRISIS")

    def test_pipeline_all_scenarios(self):
        for name in list_scenarios():
            result = run_v7_pipeline(get_scenario(name))
            self.assertTrue(result.decision)
            self.assertGreaterEqual(result.position, 0.1)
            self.assertLessEqual(result.position, 0.8)

    def test_liquidity_crisis_scenario(self):
        result = run_v7_pipeline(get_scenario("liquidity_crisis"))
        self.assertEqual(result.decision, "NO_TRADE")
        self.assertEqual(result.regime, "LIQUIDITY_CRISIS")

    def test_sideways_scenario(self):
        result = run_v7_pipeline(get_scenario("sideways_hs300"))
        self.assertEqual(result.signal, "SIDEWAYS")
        self.assertEqual(result.probability["side"], 0.5)
        self.assertEqual(result.decision, "HOLD")


if __name__ == "__main__":
    unittest.main()
