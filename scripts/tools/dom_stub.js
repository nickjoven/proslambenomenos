// dom_stub.js - the minimal DOM the repo's pages need to load under
// node. Committed once so per-session harnesses stop being retyped.
"use strict";
const ctxStub = () => new Proxy({}, {
  get: (t, k) => {
    if (k === "createImageData") return (w, h) =>
      ({data: new Uint8ClampedArray(4 * w * h), width: w, height: h});
    if (k === "measureText") return () => ({width: 10});
    if (k === "getImageData") return (x, y, w, h) =>
      ({data: new Uint8ClampedArray(4 * w * h), width: w, height: h});
    return typeof k === "string" ? (() => {}) : undefined;
  },
  set: () => true,
});
const el = () => ({
  width: 900, height: 400, style: {}, value: "0", max: 0,
  textContent: "", innerHTML: "", className: "", hidden: false,
  dataset: {}, classList: {add() {}, remove() {}, toggle() {}},
  getContext: ctxStub, addEventListener() {}, appendChild() {},
  setPointerCapture() {}, releasePointerCapture() {},
  getBoundingClientRect: () => ({left: 0, top: 0, width: 900,
                                 height: 400}),
});
global.document = {
  getElementById: el, createElement: el, querySelector: el,
  querySelectorAll: () => [], documentElement: el(),
  addEventListener() {}, body: el(),
};
global.getComputedStyle = () => ({getPropertyValue: () => "#000"});
global.matchMedia = () => ({matches: false, addEventListener() {}});
global.requestAnimationFrame = () => 0;
global.devicePixelRatio = 1;
global.innerWidth = 1200;
global.innerHeight = 800;
global.addEventListener = () => {};
global.window = global;
