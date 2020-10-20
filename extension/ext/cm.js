//create right click menu
chrome.contextMenus.create({
  id: "scrapePost",
  title: "Scrape this facebook post",
  contexts: ["selection"],
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



*/
chrome.contextMenus.onClicked.addListener(function(clickData) {
  if (clickData.menuItemId == "scrapePost") {
    console.log(clickData.linkUrl);
    chrome.tabs.create({
      url: clickData.linkUrl,
    });
    scrapePost();
    console.log("sucess");
  } else {
    console.log("failure");
  }
});

//Function to handle the scraping and automatically scrolling
function scrapePost() {
  const selectors = {
    feed: "[role='feed']",
    feed: "div[data-pagelet='root']",
    thread: "div[data-testid='Keycommand_wrapper_feed_story']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
    text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
    post: "div[data-ad-comet-preview='message']",
  };
  console.log(document.querySelector(selectors.feed));
}
