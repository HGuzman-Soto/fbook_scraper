class Model {
  constructor() {
    this.id = null;
  }

  async save() {
    let table = this.constructor.name.toLowerCase() + "s";

    this.id = md5(toDocument(this));

    let rows = await select(table);
    let found = false;

    for (let key in rows) {
      if (rows[key].id === this.id) {
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
