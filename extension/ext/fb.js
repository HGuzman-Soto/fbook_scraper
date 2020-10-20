const selectors = {
  feed: "[role='feed']",
  thread: "div[data-testid='Keycommand_wrapper_feed_story']",
  comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
  text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
  post: "div[data-ad-comet-preview='message']",
};

let feed = document.querySelector(selectors.feed);
let observer = new MutationObserver(onMutation);
// let timeout = null;

function scrapeData() {
  if (window.location.href == "https://www.facebook.com/") {
    console.log("success");

    onMutation();
    watch();
  } else {
    console.log("failure");
  }
}

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

scrapeData();
window.addEventListener("click", scrapeData);
