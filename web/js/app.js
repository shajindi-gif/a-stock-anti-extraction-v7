(function () {
  'use strict';

  const Engine = typeof V8Engine !== 'undefined' ? V8Engine : V7Engine;
  const { runV8Pipeline, toReportV8, getScenario, getScenarioOptions, decisionColor } = Engine;

  const els = {
    scenario: document.getElementById('scenario'),
    runBtn: document.getElementById('runBtn'),
    symbolName: document.getElementById('symbolName'),
    symbolCode: document.getElementById('symbolCode'),
    price: document.getElementById('price'),
    segUp: document.getElementById('segUp'),
    segSide: document.getElementById('segSide'),
    segDown: document.getElementById('segDown'),
    probUp: document.getElementById('probUp'),
    probSide: document.getElementById('probSide'),
    probDown: document.getElementById('probDown'),
    decisionBadge: document.getElementById('decisionBadge'),
    decisionLabel: document.getElementById('decisionLabel'),
    position: document.getElementById('position'),
    positionFill: document.getElementById('positionFill'),
    regime: document.getElementById('regime'),
    stopPct: document.getElementById('stopPct'),
    stopAction: document.getElementById('stopAction'),
    structureNotes: document.getElementById('structureNotes'),
    orderIntent: document.getElementById('orderIntent'),
    orderNote: document.getElementById('orderNote'),
    rebalanceAction: document.getElementById('rebalanceAction'),
    rebalanceShares: document.getElementById('rebalanceShares'),
    rebalanceDiff: document.getElementById('rebalanceDiff'),
    conditionalOrders: document.getElementById('conditionalOrders'),
    report: document.getElementById('report'),
    copyBtn: document.getElementById('copyBtn'),
  };

  function pct(n) {
    return Math.round(n * 100) + '%';
  }

  function renderV8(result) {
    const v7 = result.v7;
    const p = v7.probability;

    els.symbolName.textContent = v7.symbol;
    els.symbolCode.textContent = v7.code;
    els.price.textContent = v7.price.toFixed(3);

    els.segUp.style.width = pct(p.up);
    els.segSide.style.width = pct(p.side);
    els.segDown.style.width = pct(p.down);
    els.segUp.querySelector('span').textContent = '上涨 ' + pct(p.up);
    els.segSide.querySelector('span').textContent = '震荡 ' + pct(p.side);
    els.segDown.querySelector('span').textContent = '下跌 ' + pct(p.down);

    els.probUp.textContent = pct(p.up);
    els.probSide.textContent = pct(p.side);
    els.probDown.textContent = pct(p.down);

    const color = decisionColor(v7.decision);
    els.decisionBadge.textContent = v7.decision;
    els.decisionBadge.style.color = color;
    els.decisionBadge.style.background = color + '22';
    els.decisionLabel.textContent = v7.decision_label;

    els.position.textContent = pct(v7.position);
    els.positionFill.style.width = pct(v7.position);

    els.regime.textContent = v7.regime_label;
    els.stopPct.textContent = '-' + v7.stop_pct + '%';
    els.stopAction.textContent = v7.stop_action;

    els.structureNotes.innerHTML = v7.structure_notes
      .map(function (n) { return '<li>' + n + '</li>'; })
      .join('');

    els.orderIntent.textContent = result.order_route.action_label;
    els.orderNote.textContent = result.order_route.note;
    els.rebalanceAction.textContent = result.rebalance.action_label;
    els.rebalanceShares.textContent = result.rebalance.shares + ' 份';
    els.rebalanceDiff.textContent = (result.rebalance.diff_value >= 0 ? '+' : '') +
      result.rebalance.diff_value.toFixed(0) + ' 元';

    els.conditionalOrders.innerHTML = result.conditional_orders.length
      ? result.conditional_orders.map(function (o) {
          return '<li><strong>' + o.type + '</strong> · 触发 ' + o.trigger_price +
            ' · ' + o.quantity + '<br><span style="color:#8b949e">' + o.app_path + '</span></li>';
        }).join('')
      : '<li>当前无需设置条件单</li>';

    els.report.textContent = toReportV8(result);
  }

  function analyze() {
    renderV8(runV8Pipeline(getScenario(els.scenario.value)));
  }

  function initSelect() {
    getScenarioOptions().forEach(function (opt) {
      const option = document.createElement('option');
      option.value = opt.key;
      option.textContent = opt.label;
      els.scenario.appendChild(option);
    });
  }

  els.runBtn.addEventListener('click', analyze);
  els.scenario.addEventListener('change', analyze);

  els.copyBtn.addEventListener('click', function () {
    navigator.clipboard.writeText(els.report.textContent).then(function () {
      els.copyBtn.textContent = '已复制 ✓';
      setTimeout(function () { els.copyBtn.textContent = '复制报告'; }, 1500);
    });
  });

  initSelect();
  analyze();
})();
