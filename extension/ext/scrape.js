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

scrapePost();
