// window.addEventListener("onpagehide", () => {
//   console.log(window.location.href);
//   if (window.location.href == "https://facebook.com") {
//     console.log("success");
//     main();
//   }
// });

window.addEventListener("load", () => {
  const selectors = {
    feed: "[role='feed']",
    feed: "div[data-pagelet='root']",
    thread: "div[data-testid='Keycommand_wrapper_feed_story']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
    text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
    post: "div[data-ad-comet-preview='message']",
  };
  let timeout = null;
  let observer = new MutationObserver(onMutation);
  let feed = document.querySelector(selectors.feed);

  onMutation();
  watch();

  async function onMutation() {
    console.log("Handling mutation.");

    let threads, thread, post, cmts, doc;

    threads = sel(document, selectors.thread);

    for (thread of threads) {
      doc = new Thread();
      post = posts(thread);

      cmts = sel(thread, selectors.comments);
      post.map((em) => doc.post.push(em.textContent));
      cmts.map((em) => doc.comments.push(em.textContent));

      if (doc.comments.length) {
        await doc.save();
      }
    }
  }

  async function watch() {
    observer.observe(feed, {
      childList: true,
      subtree: true,
    });
  }

  function pause() {
    observer.disconnect();
  }

  function posts(thread) {
    return sel(thread, selectors.post);
  }

  function comments(thread) {
    return sel(thread, selectors.text);
  }
});

// main();
