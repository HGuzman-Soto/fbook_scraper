/*

Finds the comments area of the new tab and scrapes the entire page.
Runs after cm.js is called and expandAll.js finishes running

*/

function scrapePost(upperBound) {
  const selectors = {
    post: '[aria-posinset][role="article"]',
    post_text: "div[data-ad-comet-preview='message']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
  };
  console.log("scraping new tab");
  let post, cmts, doc;

  main = document.querySelector(selectors.post);
  let observer = new MutationObserver(onMutation);
  watch(main, observer)
  onMutation()
  setTimeout(function () {
    console.log("FINISHED")
    observer.disconnect();
    window.close();
    }, upperBound);

  

  async function onMutation() {
    console.log("Handling mutation.");
    doc = new Thread();
    post = posts(main);

    cmts = sel(main, selectors.comments);
    post.map((em) => doc.post.push(em.textContent));
    cmts.map((em) => doc.comments.push(em.textContent));

    if (doc.comments.length) {
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

const test = {
  num_of_comments: '.gtad4xkn'
}

comment_text = document.querySelector(test.num_of_comments).textContent
console.log("get comment_text", comment_text)
let matches = comment_text.match(/(\d+)/); 
let test2 = parseInt(matches[0])
console.log("comment number int:", test2)

var set_timeout_timer = 100;

if (test2 > 50) {
  set_timeout_timer = test2 * 110
}


console.log(set_timeout_timer)
upper_bound = set_timeout_timer * 1.5
console.log(upper_bound)

setTimeout(function () { scrapePost(upper_bound) }, set_timeout_timer)
//set a timeout based on message * time = estimated_total_time

