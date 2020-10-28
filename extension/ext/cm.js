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

    // function timeout(ms) {
    //   return new Promise((res) => setTimeout(res, ms));
    // }

    // async function fireEvents() {
    //   await timeout(7000);
    //   delay_script();
    //   await timeout(7000);
    //   scrapePost();
    // }
    // fireEvents();

    function first() {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          let test = delay_script();
          console.log(test);
          resolve("Stuff worked!");
        }, 7000);
      });
    }

    first().then(function() {
      scrapePost();
    });
  }
});

function delay_script() {
  let execute = chrome.tabs.executeScript({ file: "ext/expandAll.js" });
  console.log("finsihed this script");
  return execute;
}

function scrapePost() {
  console.log("called scrape ");
  chrome.tabs.executeScript({ file: "ext/scrape.js" });
}
