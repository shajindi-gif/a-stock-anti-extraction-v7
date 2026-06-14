"""v7 核心引擎 — 串联预测、决策、风控全流程。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from decision.ai_trader import DECISION_LABELS, ai_decision
from decision.position_adaptor import adapt_position
from prediction.next_move_model import predict_next_move
from prediction.probability_engine import Probability, calc_probability
from risk.dynamic_stop import calc_stop_pct, stop_loss
from risk.regime_guard import REGIME_LABELS, detect_regime
from signal.fused_signal import build_market_snapshot, fuse_signals


@dataclass
class V7Result:
    symbol: str
    code: str
    price: float
    signal: str
    probability: Probability
    decision: str
    decision_label: str
    position: float
    stop_pct: float
    stop_action: str
    regime: str
    regime_label: str
    structure_notes: list[str]

    def to_report(self) -> str:
        p = self.probability
        lines = [
            "",
            "🧠 A股反收割系统 v7（AI交易决策版）",
            "━━━━━━━━━━━━━━",
            f"📊 标的：{self.symbol} ({self.code})",
            f"💹 当前价：{self.price:.3f}",
            "🧠 预测结果：",
            f"  - 上涨概率：{p['up']:.0%}",
            f"  - 震荡概率：{p['side']:.0%}",
            f"  - 下跌风险：{p['down']:.0%}",
            "━━━━━━━━━━━━━━",
            "📉 AI决策：",
            f"  👉 {self.decision}（{self.decision_label}）",
            "━━━━━━━━━━━━━━",
            "💰 仓位建议：",
            f"  → {self.position:.0%}",
            "━━━━━━━━━━━━━━",
            "⚠️ 风险控制：",
            f"  → 市场状态：{self.regime_label}",
            f"  → 动态止损 -{self.stop_pct}%",
            f"  → 止损状态：{self.stop_action}",
            "━━━━━━━━━━━━━━",
            "🧨 结构判断：",
        ]
        for note in self.structure_notes:
            lines.append(f"  → {note}")
        lines.append("━━━━━━━━━━━━━━")
        lines.append("")
        lines.append("⚠️ 免责声明：本系统为结构概率决策工具，不构成投资建议。")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "code": self.code,
            "price": self.price,
            "signal": self.signal,
            "probability": dict(self.probability),
            "decision": self.decision,
            "decision_label": self.decision_label,
            "position": self.position,
            "stop_pct": self.stop_pct,
            "stop_action": self.stop_action,
            "regime": self.regime,
            "regime_label": self.regime_label,
            "structure_notes": self.structure_notes,
        }


def run_v7_pipeline(scenario: dict[str, Any]) -> V7Result:
    """执行完整 v7 决策流水线。"""
    fused = fuse_signals(
        scenario["orderbook"],
        scenario["flow"],
        scenario["sentiment"],
    )
    market = build_market_snapshot(fused)
    signal = predict_next_move(market)
    prob = calc_probability(signal)
    regime = detect_regime(
        scenario["volatility"],
        scenario["spread_pct"],
        scenario["volume_ratio"],
    )
    decision = ai_decision(prob, regime)
    position = adapt_position(prob)
    stop_pct = calc_stop_pct(scenario["volatility"])
    stop_action = stop_loss(
        scenario["price"],
        scenario["entry"],
        scenario["volatility"],
    )

    structure_notes = [
        fused["trap_label"],
        fused["flow_label"],
        f"盘口强度比 {fused['bid_strength'] / max(fused['ask_strength'], 1):.2f}",
    ]

    return V7Result(
        symbol=scenario["symbol"],
        code=scenario["code"],
        price=scenario["price"],
        signal=signal,
        probability=prob,
        decision=decision,
        decision_label=DECISION_LABELS.get(decision, decision),
        position=position,
        stop_pct=stop_pct,
        stop_action=stop_action,
        regime=regime,
        regime_label=REGIME_LABELS.get(regime, regime),
        structure_notes=structure_notes,
    )
