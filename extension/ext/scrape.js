//Function to handle the scraping and automatically scrolling
function scrapePost() {
  console.log(document);
  const selectors = {
    // first: "div[role='article]",
    test: "div[role='main']",
    first: ".cwj9ozl2.tvmbv18p",
    thread: "div[data-testid='Keycommand_wrapper_feed_story']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
    text: ".kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql",
    post: "div[data-ad-comet-preview='message']",
  };
  console.log(this.document.querySelector(selectors.first));
  console.log(document.querySelector(selectors.thread));
  console.log(this.document.querySelector(selectors.test));

  console.log(document.querySelector(selectors.post));
  console.log(document.querySelector("p"));
  // threads = sel(document, selectors.thread);
  // console.log(threads.textContent);
}

function sel(em, sel) {
  return Array.prototype.slice.call(em.querySelectorAll(sel));
}

scrapePost();
