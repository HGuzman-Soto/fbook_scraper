
/*

Finds the comments area of the new tab and scrapes the entire page.
Runs after cm.js is called and expandAll.js finishes running

*/

function scrapePost() {
  const selectors = {
    post: '[aria-posinset][role="article"]',
    post_text: "div[data-ad-comet-preview='message']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
  };
  console.log("scraping new tab");
  let post, cmts, doc;

  main = document.querySelector(selectors.post);
  let observer = new MutationObserver(onMutation);
  onMutation();
  watch(main, observer);

  async function onMutation() {
    console.log("Handling mutation.");
    doc = new Thread();
    post = posts(main);

    cmts = sel(main, selectors.comments);
    post.map((em) => doc.post.push(em.textContent));
    cmts.map((em) => doc.comments.push(em.textContent));

    if (doc.comments.length) {
      var commSize = doc.comments.length;
      localStorage.setItem("commLength", commSize);  
      doc.save();
    }

    function sel(em, sel) {
      return Array.prototype.slice.call(em.querySelectorAll(sel));
    }
    function posts(thread) {
      return sel(thread, selectors.post_text);
    }

    function comments(thread) {
      return sel(thread, selectors.comments);
    }
  }
  async function watch(main, observer) {
    observer.observe(main, {
      childList: true,
      subtree: true,
    });
  }
}
scrapePost();
