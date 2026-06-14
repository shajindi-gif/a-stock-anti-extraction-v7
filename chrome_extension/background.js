chrome.runtime.onMessage.addListener(function (msg) {
  if (msg.action === 'openPopup') {
    chrome.action.openPopup().catch(function () {});
  }
});
