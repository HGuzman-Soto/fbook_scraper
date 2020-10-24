//Comment expansion function
function TriggerSingleLink(links, index) {
    if (index >= links.length) {
        console.log("All done.");
        return;
    }
    var oLink = links[index];
    oLink.trigger('click');
    window.setTimeout(function() {
        TriggerSingleLink(links, index + 1)
    }, 500);
}

//Function to handle the scraping and automatically scrolling
function scrapePost() {
  console.log(document);
  const selectors = {
    feed: "div[data-pagelet='root']",
    // thread: ".j83agx80.cbu4d94t",
    thread: ".bp9cbjyn.j83agx80.cbu4d94t.d2edcug0",
    // thread: ".rq0escxv.l9j0dhe7.du4w35lb",
    // thread: ".rq0escxv.l9j0dhe7.du4w35lb", #left off
  };

  let feed = document.querySelector(selectors.feed);
  console.log("feed", feed);
  console.log("main thread", document.querySelectorAll(selectors.thread));
  let threads, thread, post, cmts, doc;

  threads = sel(document, selectors.thread);

  console.log(threads);

  for (thread of threads) {
    console.log(thread.textContent);
  }

  // console.log("test", threads[9].querySelector(selectors.test));

  function sel(em, sel) {
    return Array.prototype.slice.call(em.querySelectorAll(sel));
  }
}
//Comment expansion before scraping posts (not tested AT ALL)
var links = [];
$('.js-show-link').each(function() {
    var oLink = $(this);
    if ($.trim(oLink.text()).length > 0)
        links.push(oLink);
});
if (links.length > 0) {
    console.log("Expanding " + links.length + " link" + ((links.length > 1) ? "s" : "") +"...");
    TriggerSingleLink(links, 0);
} else {
    console.log("No valid expand links found.");
}

scrapePost();
