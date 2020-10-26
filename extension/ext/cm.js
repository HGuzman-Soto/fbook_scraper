//create right click menu
chrome.contextMenus.removeAll(function() {
  chrome.contextMenus.create({
    id: "scrapePost",
    title: "Scrape this facebook post",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(function(clickData) {
  if (clickData.menuItemId == "scrapePost") {
    chrome.tabs.create({
      url: clickData.linkUrl,
    });

    //delay excuation of bookmarkelet, either timer or some reload stuff  - todo - 3 seconds

    function process(callback) {
      setTimeout(delay_script, 3000);
      callback();
    }

    process(scrapePost());
  }
});

function delay_script() {
  chrome.tabs.executeScript({ file: "ext/expandAll.js" });
}

function scrapePost() {
  chrome.tabs.executeScript({ file: "ext/expandAll.js" });
}
