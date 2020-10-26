//Function to handle the scraping and automatically scrolling
//To-do, look at expandAll.js code and find appriopate selectors
//Theres need to be a way to check for when expandall.js is done and then to scrape it

function scrapePost() {
  const selectors = {
    post: '[aria-posinset][role="article"]',
    feed: "div[data-pagelet='root']",
    thread: ".bp9cbjyn.j83agx80.cbu4d94t.d2edcug0",
    comments: "._3w53,._6iiv,._7a9a",
  };

  console.log(document.querySelector(selectors.post));
  console.log(document.querySelector(selectors.comments));
  // let feed = document.querySelector(selectors.feed);
  // console.log("feed", feed);
  // console.log("main thread", document.querySelectorAll(selectors.thread));
  // let threads, thread, post, cmts, doc;

  // threads = sel(document, selectors.thread);

  // console.log(threads);

  // for (thread of threads) {
  //   console.log(thread.textContent);
  // }

  function sel(em, sel) {
    return Array.prototype.slice.call(em.querySelectorAll(sel));
  }
}

scrapePost();
