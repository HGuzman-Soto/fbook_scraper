function increment(obj, key) {
  if (!(key in obj)) {
    obj[key] = 0;
  }

  obj[key]++;
}

function rescape(str, delimiter) {
  return (str + "").replace(
    new RegExp(
      "[.\\\\+*?\\[\\^\\]$(){}=!<>|:\\" + (delimiter || "") + "-]",
      "g"
    ),
    "\\$&"
  );
}

function sel(em, sel) {
  return Array.prototype.slice.call(em.querySelectorAll(sel));
}

function toDocument(d) {
  return d.comments.join("\n");
}

async function annotate(threads) {
  let vocab = await getVocab();

  for (let tid in threads) {
    let hasKeyword = false;

    for (let cid in threads[tid].comments) {
      for (let w of vocab) {
        // console.log (new RegExp (`\b${w}\b`, 'ig'));
        threads[tid].comments[cid] = threads[tid].comments[cid].replace(
          new RegExp(`\\b(${w})\\b`, "ig"),
          `<span style="color:red">$1</span>`
        );

        if (threads[tid].comments[cid].indexOf("<span") !== -1) {
          hasKeyword = true;
        }
      }
    }

    if (!hasKeyword) {
      delete threads[tid];
    }
  }

  return Object.values(threads).filter((t) => t);
}
