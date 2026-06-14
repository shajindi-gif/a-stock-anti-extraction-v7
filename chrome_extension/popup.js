(function () {
  'use strict';

  const { runV7Pipeline, toReport, getScenario, getScenarioOptions, decisionColor } = V7Engine;

  const els = {
    scenario: document.getElementById('scenario'),
    runBtn: document.getElementById('runBtn'),
    segUp: document.getElementById('segUp'),
    segSide: document.getElementById('segSide'),
    segDown: document.getElementById('segDown'),
    symbol: document.getElementById('symbol'),
    decision: document.getElementById('decision'),
    position: document.getElementById('position'),
    stop: document.getElementById('stop'),
    report: document.getElementById('report'),
  };

  function pct(n) {
    return Math.round(n * 100) + '%';
  }

  function render(result) {
    const p = result.probability;
    els.segUp.style.width = pct(p.up);
    els.segSide.style.width = pct(p.side);
    els.segDown.style.width = pct(p.down);
    els.symbol.textContent = result.symbol + ' ' + result.price.toFixed(3);

    const color = decisionColor(result.decision);
    els.decision.textContent = result.decision;
    els.decision.style.color = color;
    els.decision.style.background = color + '22';

    els.position.textContent = pct(result.position);
    els.stop.textContent = '-' + result.stop_pct + '%';
    els.report.textContent = toReport(result);

    chrome.storage.local.set({ lastScenario: els.scenario.value });
  }

  function analyze() {
    render(runV7Pipeline(getScenario(els.scenario.value)));
  }

  getScenarioOptions().forEach(function (opt) {
    const option = document.createElement('option');
    option.value = opt.key;
    option.textContent = opt.label;
    els.scenario.appendChild(option);
  });

  chrome.storage.local.get(['lastScenario'], function (data) {
    if (data.lastScenario) {
      els.scenario.value = data.lastScenario;
    }
    analyze();
  });

  els.runBtn.addEventListener('click', analyze);
  els.scenario.addEventListener('change', analyze);
})();
