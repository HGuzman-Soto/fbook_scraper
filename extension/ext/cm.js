/*
Create the contextMenu which creates a new tab and calls scrape.js 
which scrapes the entire comments of that page
*/

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
    setTimeout(function() {
      delay_script();
    }, 8000);
  }

  function delay_script() {
    chrome.tabs.executeScript(null, { file: "ext/expandAll.js" }, function() {
      chrome.tabs.executeScript(null, { file: "ext/scrape.js" });
    });
  }

  // function scrapePost() {
  //   console.log("run");
  //   chrome.tabs.executeScript({ file: "ext/scrape.js" });
  // }
});
