/*

Finds the comments area of the new tab and scrapes the entire page.
Runs after cm.js is called and expandAll.js finishes running

*/

function scrapePost() {
  const selectors = {
    post: '[aria-posinset][role="article"]',
    feed: "div[data-pagelet='root']",
    thread: ".bp9cbjyn.j83agx80.cbu4d94t.d2edcug0",
    comments: "._3w53,._6iiv,._7a9a",
  };

  console.log(document.querySelector(selectors.post));
  console.log(document.querySelector(selectors.comments));

  function sel(em, sel) {
    return Array.prototype.slice.call(em.querySelectorAll(sel));
  }
}

scrapePost();
