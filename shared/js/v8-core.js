/**
 * A股反收割系统 v8 — 执行闭环 + 东方财富条件单（依赖 V7Engine）
 */
(function (root, factory) {
  var v7 = typeof module === 'object' && module.exports
    ? require('./v7-core.js')
    : root.V7Engine;
  var api = factory(v7);
  if (typeof module === 'object' && module.exports) {
    module.exports = Object.assign({}, v7, api);
  } else {
    root.V8Engine = Object.assign({}, v7, api);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (V7) {
  'use strict';

  var HOLDINGS = {
    '588000': { symbol: '科创50ETF', pct: 0.35, entry: 1.038 },
    '510300': { symbol: '沪深300ETF', pct: 0.20, entry: 3.86 },
    '159915': { symbol: '创业板ETF', pct: 0.10, entry: 2.18 },
  };

  function getHoldingPct(code) {
    return (HOLDINGS[code] && HOLDINGS[code].pct) || 0.5;
  }

  function routeOrder(decision, position, currentHolding) {
    currentHolding = currentHolding == null ? 0.5 : currentHolding;
    var delta = Math.round((position - currentHolding) * 100) / 100;

    if (decision === 'NO_TRADE') {
      return { intent: 'NO_ACTION', action_label: '禁止交易', target_position: position,
        current_position: currentHolding, delta: 0, lots: 0,
        note: '流动性危机，暂停一切下单' };
    }
    if (decision === 'BUY_TREND' && delta > 0.05) {
      return { intent: 'BUY', action_label: '加仓买入', target_position: position,
        current_position: currentHolding, delta: delta,
        lots: Math.max(1, Math.floor(delta * 100)),
        note: '趋势跟随，目标仓位 ' + Math.round(position * 100) + '%' };
    }
    if (decision === 'REDUCE_POSITION' || (decision === 'HOLD' && delta < -0.05)) {
      return { intent: 'SELL', action_label: '减仓卖出', target_position: position,
        current_position: currentHolding, delta: delta,
        lots: Math.max(1, delta < 0 ? Math.floor(Math.abs(delta) * 100) : Math.floor(position * 30)),
        note: '风险升高，建议减仓' };
    }
    if (decision === 'MEAN_REVERSION') {
      return { intent: 'HOLD', action_label: '震荡观望', target_position: position,
        current_position: currentHolding, delta: delta, lots: 0,
        note: '震荡结构，等待区间边界触发条件单' };
    }
    return { intent: 'HOLD', action_label: '持有观望', target_position: position,
      current_position: currentHolding, delta: delta, lots: 0,
      note: '仓位接近目标，暂不操作' };
  }

  function rebalancePlan(code, symbol, price, targetPct, portfolioValue, currentPct) {
    portfolioValue = portfolioValue || 100000;
    currentPct = currentPct == null ? 0.5 : currentPct;
    var targetValue = portfolioValue * targetPct;
    var currentValue = portfolioValue * currentPct;
    var diffValue = targetValue - currentValue;
    var shares = Math.floor(Math.abs(diffValue) / price / 100) * 100;
    var action, actionLabel;
    if (Math.abs(diffValue) < portfolioValue * 0.02) {
      action = 'KEEP'; actionLabel = '维持仓位';
    } else if (diffValue > 0) {
      action = 'INCREASE'; actionLabel = '增持';
    } else {
      action = 'DECREASE'; actionLabel = '减持';
    }
    return {
      code: code, symbol: symbol, price: price,
      portfolio_value: portfolioValue,
      current_pct: currentPct, target_pct: targetPct,
      current_value: Math.round(currentValue * 100) / 100,
      target_value: Math.round(targetValue * 100) / 100,
      diff_value: Math.round(diffValue * 100) / 100,
      shares: shares, action: action, action_label: actionLabel,
    };
  }

  function buildStopPlan(price, entry, stopPct, decision) {
    var stopPrice = Math.round(entry * (1 - stopPct / 100) * 1000) / 1000;
    var takeProfitPct = Math.round(stopPct * 2 * 10) / 10;
    var takeProfitPrice = Math.round(entry * (1 + takeProfitPct / 100) * 1000) / 1000;
    var status = price < stopPrice ? 'TRIGGERED' : 'ARMED';
    if (decision === 'NO_TRADE') status = 'DISABLED';
    var labels = { TRIGGERED: '已触发止损', ARMED: '止损已布防', DISABLED: '止损已禁用' };
    return {
      entry: entry, current_price: price, stop_pct: stopPct,
      stop_price: stopPrice, take_profit_pct: takeProfitPct,
      take_profit_price: takeProfitPrice,
      status: status, status_label: labels[status] || status,
    };
  }

  function buildConditionalOrders(code, symbol, price, decision, orderRoute, stopPlan, rebalance) {
    var orders = [];
    if (decision !== 'NO_TRADE') {
      orders.push({
        type: '止损卖出', priority: '高',
        trigger_price: stopPlan.stop_price, order_price: '市价',
        quantity: (rebalance.shares || 100) + ' 份',
        reason: '动态止损 -' + stopPlan.stop_pct + '%',
        app_path: '东方财富 APP → 交易 → 条件单 → 止损',
      });
    }
    if (decision !== 'NO_TRADE' && ['BUY_TREND', 'MEAN_REVERSION', 'HOLD'].indexOf(decision) >= 0) {
      orders.push({
        type: '止盈卖出', priority: '中',
        trigger_price: stopPlan.take_profit_price, order_price: '限价',
        quantity: Math.max(Math.floor(rebalance.shares / 2), 100) + ' 份',
        reason: '目标止盈 +' + stopPlan.take_profit_pct + '%',
        app_path: '东方财富 APP → 交易 → 条件单 → 止盈',
      });
    }
    if (orderRoute.intent === 'BUY') {
      var buyTrigger = Math.round(price * 0.998 * 1000) / 1000;
      orders.push({
        type: '定价买入', priority: '高',
        trigger_price: buyTrigger, order_price: String(buyTrigger),
        quantity: orderRoute.lots * 100 + ' 份',
        reason: orderRoute.note,
        app_path: '东方财富 APP → 交易 → 条件单 → 定价买入',
      });
    }
    if (orderRoute.intent === 'SELL') {
      orders.push({
        type: '定价卖出', priority: '高',
        trigger_price: Math.round(price * 1.002 * 1000) / 1000,
        order_price: '市价', quantity: orderRoute.lots * 100 + ' 份',
        reason: orderRoute.note,
        app_path: '东方财富 APP → 交易 → 条件单 → 定价卖出',
      });
    }
    if (decision === 'HOLD' || decision === 'REDUCE_POSITION') {
      orders.push({
        type: '回落卖出', priority: '中',
        trigger_price: Math.round(price * 0.99 * 1000) / 1000,
        order_price: '市价',
        quantity: Math.max(Math.floor(rebalance.shares / 2), 100) + ' 份',
        reason: '从近期高点回落 1% 自动减仓',
        app_path: '东方财富 APP → 交易 → 条件单 → 回落卖出',
      });
    }
    return orders;
  }

  function formatEastmoneyGuide(orders) {
    if (!orders.length) return '当前无需设置条件单。';
    var lines = ['', '📱 东方财富条件单建议', '━━━━━━━━━━━━━━'];
    orders.forEach(function (o, i) {
      lines.push('【条件单 ' + (i + 1) + '】' + o.type + '（优先级：' + o.priority + '）');
      lines.push('  触发价：' + o.trigger_price + ' · 数量：' + o.quantity);
      lines.push('  理由：' + o.reason);
      lines.push('  操作路径：' + o.app_path);
      lines.push('');
    });
    lines.push('━━━━━━━━━━━━━━');
    lines.push('💡 请在东方财富 APP 手动设置，本系统不自动下单。');
    return lines.join('\n');
  }

  function runV8Pipeline(scenario, opts) {
    opts = opts || {};
    var v7 = V7.runV7Pipeline(scenario);
    var holding = opts.currentHolding != null ? opts.currentHolding : getHoldingPct(v7.code);
    var pv = opts.portfolioValue || 100000;
    var orderRoute = routeOrder(v7.decision, v7.position, holding);
    var rebalance = rebalancePlan(v7.code, v7.symbol, v7.price, v7.position, pv, holding);
    var stopPlan = buildStopPlan(v7.price, scenario.entry, v7.stop_pct, v7.decision);
    var conditionalOrders = buildConditionalOrders(
      v7.code, v7.symbol, v7.price, v7.decision, orderRoute, stopPlan, rebalance
    );
    var eastmoneyGuide = formatEastmoneyGuide(conditionalOrders);
    return {
      v7: v7, order_route: orderRoute, rebalance: rebalance,
      stop_plan: stopPlan, conditional_orders: conditionalOrders,
      eastmoney_guide: eastmoneyGuide, version: '8.0.0',
    };
  }

  function toReportV8(result) {
    var v7Report = V7.toReport(result.v7).replace(
      '🧠 A股反收割系统 v7（AI交易决策版）',
      '🚀 A股反收割系统 v8（自动交易闭环版）'
    );
    var r = result;
    return v7Report + '\n\n🔄 v8 执行闭环\n━━━━━━━━━━━━━━\n' +
      '📦 订单路由：' + r.order_route.action_label + '（' + r.order_route.intent + '）\n' +
      '  → ' + r.order_route.note + '\n' +
      '⚖️ 仓位重平衡：' + r.rebalance.action_label + '\n' +
      '  → 调仓份数：' + r.rebalance.shares + ' 份\n' +
      '🛡️ 自动止损：' + r.stop_plan.status_label + '\n' +
      r.eastmoney_guide;
  }

  return {
    runV8Pipeline: runV8Pipeline,
    toReportV8: toReportV8,
    routeOrder: routeOrder,
    rebalancePlan: rebalancePlan,
    buildStopPlan: buildStopPlan,
    buildConditionalOrders: buildConditionalOrders,
    formatEastmoneyGuide: formatEastmoneyGuide,
  };
});
