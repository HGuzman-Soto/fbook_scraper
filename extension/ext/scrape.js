
/*

1) Finds the comments area of the new tab and scrapes the entire page.
2) Runs after cm.js is called
3) There is a delay before the scraper starts tracking changes in the Dom Tree (lowerBound)
4) And a delay for when the scraper will stop (UpperBound). This is to resolve infinite loop issues

*/

function scrapePost(upperBound) {
  const selectors = {
    post: "[class=\"lzcic4wl\"][role=\"article\"]",
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

const find_comments = {
  comment_div: '.gtad4xkn'
}

comment_text = document.querySelector(find_comments.comment_div).textContent


//Edge case -- When the comment is < 1k
let isThousand = false;
console.log(comment_text)
if (comment_text.includes("K")) {
  isThousand = true
}

let onlyDigits = comment_text.replace(/\D/g, "");
let num_of_comments = parseInt(onlyDigits)
console.log(num_of_comments)

if (isThousand) {
  num_of_comments = num_of_comments * 100
}
console.log("comment number int:", num_of_comments)

let lowerBound = 0;


//the scaling of the second term could be a bit lower??
if (num_of_comments > 50) {
  lowerBound = ((-1 * num_of_comments / 10) ** 2) + (num_of_comments * 45) + 8000
  console.log("time:", lowerBound/1000, "seconds")

}

upperBound = 2000
setTimeout(function () { scrapePost(upperBound) }, lowerBound)

