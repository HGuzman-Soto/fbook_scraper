/*

Finds the comments area of the new tab and scrapes the entire page.
Runs after cm.js is called and expandAll.js finishes running

*/

function scrapePost(timer) {
  const selectors = {
    post: '[aria-posinset][role="article"]',
    post_text: "div[data-ad-comet-preview='message']",
    comments: ".ecm0bbzt.e5nlhep0.a8c37x1j",
  };
  console.log("scraping new tab");
  let post, cmts, doc;

  main = document.querySelector(selectors.post);
  // let observer = new MutationObserver(onMutation);
  setTimeout(test_this_out(main), timer)
  

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


  function test_this_out(main) {
    let observer = new MutationObserver(onMutation)
    onMutation();
    watch(main, observer)
  }
}

// const num_of_comments = 'd2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.oi732d6d.ik7dh3pa.fgxwclzu a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.iv3no6db.jq4qci2q.a3bd9o3v.knj5qynh.m9osqain'
const test = {
  num_of_comments: '.gtad4xkn'
}

comment_text = document.querySelector(test.num_of_comments).textContent

console.log(comment_text)
let matches = comment_text.match(/(\d+)/); 
let test2 = parseInt(matches[0])
console.log(test2)

var set_timeout_timer = 100;

if (test2 > 50) {
  set_timeout_timer = 10000
}


console.log(set_timeout_timer)

//set a timeout based on message * time = estimated_total_time
scrapePost(set_timeout_timer);

