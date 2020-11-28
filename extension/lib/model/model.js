class Model {
  constructor() {
    this.id = null;
    this.commentid = null;
  }

  async save() {
    var commentsLen = localStorage.getItem("commLength");
    var numComments = commentsLen;
    let table = this.constructor.name.toLowerCase() + "s";
    this.id = md5(toDocument(this));
    var i;
    var commentArr = [];
    for (i = 0; i < numComments; i++) {
      var char ='abcdefghijklmnopqrstuvwxyz'.charAt(i);
      commentArr.push(md5(toDocument(this) + char));
    }
    this.commentid = commentArr;
    let rows = await select(table);
    let found = false;

    for (let key in rows) {
      if (rows[key].id === this.id ) {
        rows[key] = this;
        found = true;
      }
    }

    if (!found) {
      rows.push(this);
    }

    return save(table, rows);
  }
}

