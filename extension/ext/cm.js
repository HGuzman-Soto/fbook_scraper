//create right click menu
chrome.contextMenus.removeAll(function() {
  chrome.contextMenus.create({
    id: "scrapePost",
    title: "Scrape this facebook post",
    contexts: ["selection"],
  });
});

/*
Event listener for when contextMenu is clicked

Assuming correct use-case which is when the contextMenu is clicked for a facebook
post hour (clicking this will take you to a new page with the url of the exact post)


1) Open a new tab and redirect to this new page
2) Adapt the functions from fb.js to scrape this single post
This entails modifying our css selectors and also coding functionality that makes 
the browser automatically collect all the post. This would be done, by finding the more comments
button and continously clicking it
3) Error checking -> make sure the contextMenu is click in the correct place


The scraping will have two pass
First, it will find the all comments bar and click it 
Then, it will expand all the see more, replies, and view more comments buttons until none exist
Finally, it will collect scrape all the comments

*/
chrome.contextMenus.onClicked.addListener(function(clickData) {
  if (clickData.menuItemId == "scrapePost") {
    console.log(clickData.linkUrl);
    chrome.tabs.create({
      url: clickData.linkUrl,
    });
    console.log("success");

    //here we gotta find the tab of the window that it just opened
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id + 1, {
        test: clickData.linkUrl,
      });
      console.log("testing");
      console.log(tabs[0].id);
    });
  } else {
    console.log("failure");
  }
});
