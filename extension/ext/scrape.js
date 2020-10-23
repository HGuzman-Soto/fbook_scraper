//Function to handle the scraping and automatically scrolling
function scrapePost() {
  console.log(document);
  const selectors = {
    // first: "div[role='article]",
    feed: "div[role='root']",
    // thread: ".d2edcug0.oh7imozk.tr9rh885.abvwweq7.ejjq64ki",
    test: ".du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0",
    // thread: ".rq0escxv.lpgh02oy.du4w35lb.rek2kq2y",
    thread: ".j83agx80.cbu4d94t",
    // test: ".j83agx80.l9j0dhe7.k4urcfbm",
    work: ".stjgntxs.ni8dbmo4.l82x9zwi.uo3d90p7.h905i5nu.monazrh9",

    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
    text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
    post: "div[data-ad-comet-preview='message']",
  };

  let feed = document.querySelector(selectors.feed);
  console.log(feed.querySelector(selectors.work));
  console.log("feed", feed);
  console.log("main thread", document.querySelector(selectors.thread));
  let threads, thread, post, cmts, doc;
  console.log(sel(document, selectors.work));

  threads = sel(document, selectors.thread);
  console.log(threads);
  console.log("threads", threads[9]);

  console.log("test", threads[9].querySelector(selectors.test));

  for (thread of threads) {
    doc = new Thread();
    post = posts(thread);
    console.log("post", post);

    cmts = sel(thread, selectors.comments);
    post.map((em) => doc.post.push(em.textContent));
    cmts.map((em) => doc.comments.push(em.textContent));
    console.log("posts mpa", post);
    console.log("comments", cmts);
    // if (doc.comments.length) {
    //   doc.save();
    // }
  }
}

function sel(em, sel) {
  return Array.prototype.slice.call(em.querySelectorAll(sel));
}

scrapePost();
