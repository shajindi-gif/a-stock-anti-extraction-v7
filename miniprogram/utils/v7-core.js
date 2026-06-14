/**
 * A股反收割系统 v7 — 跨平台 JS 核心引擎
 * 支持：Web / Chrome Extension / 微信小程序 (CommonJS)
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V7Engine = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const DECISION_LABELS = {
    NO_TRADE: '禁止交易（流动性危机）',
    BUY_TREND: '趋势跟随',
    REDUCE_POSITION: '减仓避险',
    MEAN_REVERSION: '均值回归',
    HOLD: '观望持有',
  };

  const REGIME_LABELS = {
    NORMAL: '正常',
    HIGH_VOLATILITY: '高波动',
    LIQUIDITY_CRISIS: '流动性危机',
  };

  const SCENARIO_LABELS = {
    bullish_kcb50: '科创50ETF · 多头结构',
    sideways_hs300: '沪深300ETF · 震荡结构',
    bear_trap_detected: '创业板ETF · 诱多检测',
    liquidity_crisis: '科创50ETF · 流动性危机',
  };

  const DEMO_SCENARIOS = {
    bullish_kcb50: {
      symbol: '科创50ETF',
      code: '588000',
      price: 1.052,
      entry: 1.038,
      volatility: 1.15,
      spread_pct: 0.08,
      volume_ratio: 1.2,
      orderbook: {
        bids: { 1.051: 85000, 1.05: 120000, 1.049: 95000 },
        asks: { 1.052: 42000, 1.053: 38000, 1.054: 51000 },
      },
      flow: {
        direction: 'inflow',
        label: '资金流入中',
        aggressive_buy: 156000,
        aggressive_sell: 89000,
      },
      sentiment: { trap: 'none', trap_label: '无明显诱多' },
    },
    sideways_hs300: {
      symbol: '沪深300ETF',
      code: '510300',
      price: 3.856,
      entry: 3.86,
      volatility: 0.95,
      spread_pct: 0.05,
      volume_ratio: 0.85,
      orderbook: {
        bids: { 3.855: 58000, 3.854: 55000, 3.853: 57000 },
        asks: { 3.856: 62000, 3.857: 61000, 3.858: 64000 },
      },
      flow: {
        direction: 'inflow',
        label: '资金小幅流入',
        aggressive_buy: 65000,
        aggressive_sell: 72000,
      },
      sentiment: { trap: 'none', trap_label: '无明显诱多' },
    },
    bear_trap_detected: {
      symbol: '创业板ETF',
      code: '159915',
      price: 2.145,
      entry: 2.18,
      volatility: 1.8,
      spread_pct: 0.12,
      volume_ratio: 0.55,
      orderbook: {
        bids: { 2.144: 45000, 2.143: 38000, 2.142: 42000 },
        asks: { 2.145: 88000, 2.146: 92000, 2.147: 76000 },
      },
      flow: {
        direction: 'outflow',
        label: '资金流出',
        aggressive_buy: 35000,
        aggressive_sell: 98000,
      },
      sentiment: { trap: 'bull_trap', trap_label: '⚠️ 检测到诱多结构' },
    },
    liquidity_crisis: {
      symbol: '科创50ETF',
      code: '588000',
      price: 0.985,
      entry: 1.02,
      volatility: 2.5,
      spread_pct: 0.65,
      volume_ratio: 0.15,
      orderbook: {
        bids: { 0.984: 8000, 0.983: 5000, 0.982: 3000 },
        asks: { 0.985: 12000, 0.986: 9000, 0.987: 7000 },
      },
      flow: {
        direction: 'outflow',
        label: '恐慌性流出',
        aggressive_buy: 12000,
        aggressive_sell: 85000,
      },
      sentiment: { trap: 'panic_sell', trap_label: '⚠️ 恐慌抛售结构' },
    },
  };

  function sumValues(obj) {
    return Object.values(obj || {}).reduce((a, b) => a + b, 0);
  }

  function fuseSignals(orderbook, flow, sentiment) {
    const bidTotal = sumValues(orderbook.bids);
    const askTotal = sumValues(orderbook.asks);
    return {
      bid_strength: bidTotal,
      ask_strength: askTotal,
      flow: flow.direction || 'neutral',
      aggressive_buy: flow.aggressive_buy || 0,
      aggressive_sell: flow.aggressive_sell || 0,
      trap: sentiment.trap || 'none',
      flow_label: flow.label || '中性',
      trap_label: sentiment.trap_label || '无明显诱多',
    };
  }

  function buildMarketSnapshot(fused) {
    return {
      bid_strength: fused.bid_strength,
      ask_strength: fused.ask_strength,
      flow: fused.flow,
      aggressive_buy: fused.aggressive_buy,
      aggressive_sell: fused.aggressive_sell,
      trap: fused.trap,
    };
  }

  function predictNextMove(market) {
    let score = 0;
    if (market.bid_strength > market.ask_strength) score += 1;
    if (market.flow === 'inflow') score += 1;
    if (market.aggressive_buy > market.aggressive_sell) score += 1;
    if (market.trap === 'none') score += 1;
    else score -= 2;
    if (score >= 3) return 'UP_PROB_HIGH';
    if (score === 2) return 'SIDEWAYS';
    return 'DOWN_RISK';
  }

  function calcProbability(signal) {
    if (signal === 'UP_PROB_HIGH') return { up: 0.7, side: 0.2, down: 0.1 };
    if (signal === 'SIDEWAYS') return { up: 0.3, side: 0.5, down: 0.2 };
    return { up: 0.2, side: 0.3, down: 0.5 };
  }

  function detectRegime(volatility, spreadPct, volumeRatio) {
    if (spreadPct > 0.5 || volumeRatio < 0.3) return 'LIQUIDITY_CRISIS';
    if (volatility > 1.5) return 'HIGH_VOLATILITY';
    return 'NORMAL';
  }

  function aiDecision(prob, regime) {
    if (regime === 'LIQUIDITY_CRISIS') return 'NO_TRADE';
    if (prob.up > 0.65) return 'BUY_TREND';
    if (prob.down > 0.6) return 'REDUCE_POSITION';
    if (prob.side > 0.5) return 'MEAN_REVERSION';
    return 'HOLD';
  }

  function adaptPosition(prob) {
    let base = 0.5 + (prob.up - 0.5);
    if (base > 0.8) return 0.8;
    if (base < 0.1) return 0.1;
    return Math.round(base * 100) / 100;
  }

  function calcStopPct(volatility) {
    return Math.round(0.02 * volatility * 1000) / 10;
  }

  function stopLoss(price, entry, volatility) {
    if (price < entry * (1 - 0.02 * volatility)) return 'STOP_OUT';
    return 'HOLD';
  }

  function pct(n) {
    return Math.round(n * 100) + '%';
  }

  function runV7Pipeline(scenario) {
    const fused = fuseSignals(scenario.orderbook, scenario.flow, scenario.sentiment);
    const market = buildMarketSnapshot(fused);
    const signal = predictNextMove(market);
    const probability = calcProbability(signal);
    const regime = detectRegime(scenario.volatility, scenario.spread_pct, scenario.volume_ratio);
    const decision = aiDecision(probability, regime);
    const position = adaptPosition(probability);
    const stopPct = calcStopPct(scenario.volatility);
    const stopAction = stopLoss(scenario.price, scenario.entry, scenario.volatility);
    const structureNotes = [
      fused.trap_label,
      fused.flow_label,
      '盘口强度比 ' + (fused.bid_strength / Math.max(fused.ask_strength, 1)).toFixed(2),
    ];

    return {
      symbol: scenario.symbol,
      code: scenario.code,
      price: scenario.price,
      signal,
      probability,
      decision,
      decision_label: DECISION_LABELS[decision] || decision,
      position,
      stop_pct: stopPct,
      stop_action: stopAction,
      regime,
      regime_label: REGIME_LABELS[regime] || regime,
      structure_notes: structureNotes,
    };
  }

  function toReport(result) {
    const p = result.probability;
    const lines = [
      '',
      '🧠 A股反收割系统 v7（AI交易决策版）',
      '━━━━━━━━━━━━━━',
      '📊 标的：' + result.symbol + ' (' + result.code + ')',
      '💹 当前价：' + result.price.toFixed(3),
      '🧠 预测结果：',
      '  - 上涨概率：' + pct(p.up),
      '  - 震荡概率：' + pct(p.side),
      '  - 下跌风险：' + pct(p.down),
      '━━━━━━━━━━━━━━',
      '📉 AI决策：',
      '  👉 ' + result.decision + '（' + result.decision_label + '）',
      '━━━━━━━━━━━━━━',
      '💰 仓位建议：',
      '  → ' + pct(result.position),
      '━━━━━━━━━━━━━━',
      '⚠️ 风险控制：',
      '  → 市场状态：' + result.regime_label,
      '  → 动态止损 -' + result.stop_pct + '%',
      '  → 止损状态：' + result.stop_action,
      '━━━━━━━━━━━━━━',
      '🧨 结构判断：',
    ];
    result.structure_notes.forEach(function (note) {
      lines.push('  → ' + note);
    });
    lines.push('━━━━━━━━━━━━━━');
    lines.push('');
    lines.push('⚠️ 免责声明：本系统为结构概率决策工具，不构成投资建议。');
    return lines.join('\n');
  }

  function getScenario(name) {
    const s = DEMO_SCENARIOS[name] || DEMO_SCENARIOS.bullish_kcb50;
    return JSON.parse(JSON.stringify(s));
  }

  function listScenarios() {
    return Object.keys(DEMO_SCENARIOS);
  }

  function getScenarioOptions() {
    return listScenarios().map(function (key) {
      return { key: key, label: SCENARIO_LABELS[key] || key };
    });
  }

  function decisionColor(decision) {
    const map = {
      BUY_TREND: '#3fb950',
      MEAN_REVERSION: '#d29922',
      REDUCE_POSITION: '#f85149',
      NO_TRADE: '#f85149',
      HOLD: '#8b949e',
    };
    return map[decision] || '#58a6ff';
  }

  return {
    DECISION_LABELS,
    REGIME_LABELS,
    SCENARIO_LABELS,
    DEMO_SCENARIOS,
    runV7Pipeline,
    toReport,
    getScenario,
    listScenarios,
    getScenarioOptions,
    decisionColor,
  };
});
