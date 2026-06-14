(function () {
  'use strict';

  const Engine = typeof V8Engine !== 'undefined' ? V8Engine : V7Engine;
  const { runV8Pipeline, toReportV8, getScenario, getScenarioOptions, decisionColor } = Engine;

  const els = {
    scenario: document.getElementById('scenario'),
    runBtn: document.getElementById('runBtn'),
    segUp: document.getElementById('segUp'),
    segSide: document.getElementById('segSide'),
    segDown: document.getElementById('segDown'),
    symbol: document.getElementById('symbol'),
    decision: document.getElementById('decision'),
    orderRoute: document.getElementById('orderRoute'),
    condCount: document.getElementById('condCount'),
    condList: document.getElementById('condList'),
    report: document.getElementById('report'),
  };

  function pct(n) {
    return Math.round(n * 100) + '%';
  }

  function render(result) {
    const v7 = result.v7;
    const p = v7.probability;
    els.segUp.style.width = pct(p.up);
    els.segSide.style.width = pct(p.side);
    els.segDown.style.width = pct(p.down);
    els.symbol.textContent = v7.symbol + ' ' + v7.price.toFixed(3);

    const color = decisionColor(v7.decision);
    els.decision.textContent = v7.decision;
    els.decision.style.color = color;
    els.decision.style.background = color + '22';

    els.orderRoute.textContent = result.order_route.action_label;
    els.condCount.textContent = result.conditional_orders.length + ' 条';

    els.condList.innerHTML = result.conditional_orders.map(function (o) {
      return '<div class="cond-item"><b>' + o.type + '</b> @ ' + o.trigger_price + '</div>';
    }).join('');

    els.report.textContent = toReportV8(result);
    chrome.storage.local.set({ lastScenario: els.scenario.value });
  }

  function analyze() {
    render(runV8Pipeline(getScenario(els.scenario.value)));
  }

  getScenarioOptions().forEach(function (opt) {
    const option = document.createElement('option');
    option.value = opt.key;
    option.textContent = opt.label;
    els.scenario.appendChild(option);
  });

  chrome.storage.local.get(['lastScenario'], function (data) {
    if (data.lastScenario) els.scenario.value = data.lastScenario;
    analyze();
  });

  els.runBtn.addEventListener('click', analyze);
  els.scenario.addEventListener('change', analyze);
})();
