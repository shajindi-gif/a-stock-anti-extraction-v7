(function () {
  'use strict';

  const { runV7Pipeline, toReport, getScenario, getScenarioOptions, decisionColor } = V7Engine;

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
    report: document.getElementById('report'),
    copyBtn: document.getElementById('copyBtn'),
  };

  function pct(n) {
    return Math.round(n * 100) + '%';
  }

  function render(result) {
    const p = result.probability;

    els.symbolName.textContent = result.symbol;
    els.symbolCode.textContent = result.code;
    els.price.textContent = result.price.toFixed(3);

    els.segUp.style.width = pct(p.up);
    els.segSide.style.width = pct(p.side);
    els.segDown.style.width = pct(p.down);
    els.segUp.querySelector('span').textContent = '上涨 ' + pct(p.up);
    els.segSide.querySelector('span').textContent = '震荡 ' + pct(p.side);
    els.segDown.querySelector('span').textContent = '下跌 ' + pct(p.down);

    els.probUp.textContent = pct(p.up);
    els.probSide.textContent = pct(p.side);
    els.probDown.textContent = pct(p.down);

    const color = decisionColor(result.decision);
    els.decisionBadge.textContent = result.decision;
    els.decisionBadge.style.color = color;
    els.decisionBadge.style.background = color + '22';
    els.decisionLabel.textContent = result.decision_label;

    els.position.textContent = pct(result.position);
    els.positionFill.style.width = pct(result.position);

    els.regime.textContent = result.regime_label;
    els.stopPct.textContent = '-' + result.stop_pct + '%';
    els.stopAction.textContent = result.stop_action;

    els.structureNotes.innerHTML = result.structure_notes
      .map(function (n) { return '<li>' + n + '</li>'; })
      .join('');

    els.report.textContent = toReport(result);
  }

  function analyze() {
    const key = els.scenario.value;
    render(runV7Pipeline(getScenario(key)));
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
