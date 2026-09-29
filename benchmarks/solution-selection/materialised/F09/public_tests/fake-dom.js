'use strict';
// Minimal fake DOM for controller tests: focus follows browser rules (hidden, disabled or
// disconnected elements cannot take focus; disabling the focused element drops focus to body).

class FakeElement {
  constructor(document, id, parent = null) {
    this.ownerDocument = document;
    this.id = id;
    this.parent = parent;
    this.hidden = false;
    this._disabled = false;
    this._connected = true;
    this.attributes = {};
    this.textContent = '';
  }
  get isConnected() {
    for (let node = this; node; node = node.parent) if (!node._connected) return false;
    return true;
  }
  get disabled() { return this._disabled; }
  set disabled(value) {
    this._disabled = Boolean(value);
    if (this._disabled && this.ownerDocument.activeElement === this) this.ownerDocument.activeElement = this.ownerDocument.body;
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
  removeAttribute(name) { delete this.attributes[name]; }
  contains(other) {
    for (let node = other; node; node = node.parent) if (node === this) return true;
    return false;
  }
  focus() {
    if (!this.isConnected || this._disabled) return;
    for (let node = this; node; node = node.parent) if (node.hidden) return;
    this.ownerDocument.activeElement = this;
  }
  remove() {
    this._connected = false;
    if (this.contains(this.ownerDocument.activeElement)) this.ownerDocument.activeElement = this.ownerDocument.body;
  }
}

function buildPage() {
  const document = { body: null, activeElement: null };
  document.body = new FakeElement(document, 'body');
  document.activeElement = document.body;
  const main = new FakeElement(document, 'main', document.body);
  const el = (id, parent) => new FakeElement(document, id, parent);
  const page = {
    document,
    heading: el('page-heading', main),
    trigger: el('delete-account', main),
    dialog: el('confirm-dialog', main),
  };
  page.dialog.hidden = true;
  page.title = el('confirm-title', page.dialog);
  page.errorRegion = el('confirm-error', page.dialog);
  page.confirmButton = el('confirm-ok', page.dialog);
  page.cancelButton = el('confirm-cancel', page.dialog);
  return page;
}

module.exports = { FakeElement, buildPage };
