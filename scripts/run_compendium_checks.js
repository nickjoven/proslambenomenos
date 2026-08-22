#!/usr/bin/env node
// Headless runner for the compendium's verification checks (G1 fix):
// loads compendium/index.html, stubs the DOM, executes the page's own
// <script>, and runs every registered check. LAW-17: every check must
// also declare at least one named MUTANT (a knob set to a specific
// wrong value) and FAIL under each; the registered id set must equal
// the page's data-verify buttons; Math.random is seeded. Exit 0 iff
// all pass, all mutants fail, and the id sets agree.

"use strict";
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(
  path.join(__dirname, "..", "compendium", "index.html"), "utf8");
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
const pageIds = [...new Set([...html.matchAll(/data-verify="(c\d+)"/g)].map(m => m[1]))].sort();

// seeded LCG so falsifier runs are reproducible
let seed = 0x2545F491;
Math.random = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };

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

eval(script + "\n;global.__CHECKS = CHECKS; global.__MUTANTS = MUTANTS; global.__KNOBS = KNOBS;");

const run = id => {
  try { return global.__CHECKS[id](); }
  catch (e) { return { pass: false, lines: ["exception: " + e.message] }; }
};
const resetKnobs = () => { for (const k of Object.keys(global.__KNOBS)) delete global.__KNOBS[k]; };

let passed = 0, mutantsRun = 0, mutantsFailed = 0, missingMutants = [];
const ids = Object.keys(global.__CHECKS).sort();
for (const id of ids) {
  resetKnobs();
  const r = run(id);
  if (r.pass) passed++;
  else { console.log(`${id}: FAIL`); (r.lines || []).forEach(l => console.log("   ", l)); }
  const muts = global.__MUTANTS[id] || {};
  if (!Object.keys(muts).length) missingMutants.push(id);
  for (const [name, apply] of Object.entries(muts)) {
    resetKnobs(); apply();
    const m = run(id);
    mutantsRun++;
    if (!m.pass) mutantsFailed++;
    else console.log(`${id}: mutant '${name}' PASSES (bad - the check does not test this discriminator)`);
  }
}
resetKnobs();
const idsOK = JSON.stringify(ids) === JSON.stringify(pageIds);
if (!idsOK) console.log(`registered ids ${JSON.stringify(ids)} != page buttons ${JSON.stringify(pageIds)}`);
if (missingMutants.length) console.log(`checks without a mutant: ${missingMutants.join(", ")}`);
console.log(`compendium checks: ${passed}/${ids.length} pass; mutants ${mutantsFailed}/${mutantsRun} fail as required; id set matches page: ${idsOK}`);
const ok = passed === ids.length && mutantsFailed === mutantsRun && !missingMutants.length && idsOK;
process.exit(ok ? 0 : 2);
