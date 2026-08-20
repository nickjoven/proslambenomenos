#!/usr/bin/env node
// Headless runner for the compendium's verification checks (G1 fix):
// loads compendium/index.html, stubs the DOM, executes the page's own
// <script>, and runs every registered check. Exit 0 iff all pass.
// This is the same evidence the claim files cite — now re-runnable
// from the tree by anyone, forever.

"use strict";
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(
  path.join(__dirname, "..", "compendium", "index.html"), "utf8");
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];

const noop = () => {};
const ctxStub = new Proxy({}, { get: (t, k) => (k === "canvas" ? {} : noop) });
const elStub = () => new Proxy(
  { style: {}, classList: { add: noop, remove: noop } },
  {
    get: (t, k) => {
      if (k in t) return t[k];
      if (k === "getContext") return () => ctxStub;
      if (k === "addEventListener") return noop;
      if (k === "value") return "17";
      if (k === "width") return 780;
      if (k === "height") return 300;
      if (k === "dataset") return {};
      if (k === "querySelector") return elStub;
      return noop;
    },
    set: () => true,
  });

global.document = {
  getElementById: elStub,
  querySelectorAll: () => [],
  documentElement: {},
};
global.getComputedStyle = () => ({ getPropertyValue: () => "#000" });
global.matchMedia = () => ({ addEventListener: noop });

eval(script + "\n;global.__CHECKS = CHECKS;");

let passed = 0;
const ids = Object.keys(global.__CHECKS);
for (const id of ids) {
  let r;
  try { r = global.__CHECKS[id](); }
  catch (e) { r = { pass: false, lines: ["exception: " + e.message] }; }
  if (r.pass) { passed++; }
  else {
    console.log(`${id}: FAIL`);
    (r.lines || []).forEach((l) => console.log("   ", l));
  }
}
console.log(`compendium checks: ${passed}/${ids.length} pass`);
process.exit(passed === ids.length ? 0 : 2);
