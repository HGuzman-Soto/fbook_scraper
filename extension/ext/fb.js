
/*

Script automatically runs in the facebook home page and collects seeable data
This only runs in on the home page.

*/

const selectors = {
  feed: "[role='feed']",
  thread: ".j83agx80.l9j0dhe7.k4urcfbm",
  comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
  text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
  post: "div[data-ad-comet-preview='message']",
};

function scrapeData() {
  if (window.location.href == "https://www.facebook.com/") {
    console.log("success");
    let feed = document.querySelector(selectors.feed);
    let observer = new MutationObserver(onMutation);
    onMutation();
    watch(feed, observer);
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
      var commSize = doc.comments.length;
      localStorage.setItem("commLength", commSize);
      await doc.save();
    }
  }
}

async function watch(feed, observer) {
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
