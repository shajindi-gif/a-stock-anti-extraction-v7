(function () {
  'use strict';

  function injectBadge() {
    if (document.getElementById('v7-anti-harvest-badge')) return;

    const badge = document.createElement('div');
    badge.id = 'v7-anti-harvest-badge';
    badge.innerHTML = '🧠 v7 AI决策';
    badge.title = '点击打开 A股反收割系统 v7 插件';
    badge.addEventListener('click', function () {
      chrome.runtime.sendMessage({ action: 'openPopup' });
    });
    document.body.appendChild(badge);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBadge);
  } else {
    injectBadge();
  }
})();
