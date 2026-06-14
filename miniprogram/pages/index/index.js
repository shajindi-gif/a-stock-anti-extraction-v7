const V7 = require('../../utils/v7-core.js');

Page({
  data: {
    scenarioKeys: [],
    scenarioLabels: [],
    scenarioIndex: 0,
    loading: false,
    result: {
      symbol: '—',
      code: '',
      price: '—',
      decision: '—',
      decision_label: '',
      regime_label: '',
      stop_pct: 0,
      stop_action: '',
      structure_notes: [],
    },
    probUp: '0%',
    probSide: '0%',
    probDown: '0%',
    probUpPct: 0,
    probSidePct: 0,
    probDownPct: 0,
    positionPct: '0%',
    decisionColor: '#58a6ff',
    decisionBg: '#58a6ff22',
    reportText: '',
  },

  onLoad() {
    const options = V7.getScenarioOptions();
    this.setData({
      scenarioKeys: options.map((o) => o.key),
      scenarioLabels: options.map((o) => o.label),
    });
    this.runAnalysis();
  },

  onScenarioChange(e) {
    this.setData({ scenarioIndex: Number(e.detail.value) });
    this.runAnalysis();
  },

  runAnalysis() {
    const key = this.data.scenarioKeys[this.data.scenarioIndex];
    const result = V7.runV7Pipeline(V7.getScenario(key));
    const p = result.probability;

    this.setData({
      loading: false,
      result: {
        ...result,
        price: result.price.toFixed(3),
      },
      probUp: this.pct(p.up),
      probSide: this.pct(p.side),
      probDown: this.pct(p.down),
      probUpPct: Math.round(p.up * 100),
      probSidePct: Math.round(p.side * 100),
      probDownPct: Math.round(p.down * 100),
      positionPct: this.pct(result.position),
      decisionColor: V7.decisionColor(result.decision),
      decisionBg: V7.decisionColor(result.decision) + '22',
      reportText: V7.toReport(result),
    });
  },

  pct(n) {
    return Math.round(n * 100) + '%';
  },

  copyReport() {
    wx.setClipboardData({
      data: this.data.reportText,
      success: () => wx.showToast({ title: '已复制', icon: 'success' }),
    });
  },
});
