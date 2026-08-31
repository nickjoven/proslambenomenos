#!/usr/bin/env bash
# jstest.sh - extract the <script> body of an HTML page, syntax-check
# it, and (if it exports a runAll or is otherwise loadable) run it
# under node with the committed DOM stub.
#
# Usage: scripts/tools/jstest.sh <page.html>
set -euo pipefail
PAGE=${1:?usage: jstest.sh <page.html>}
TOOLS_DIR=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp /tmp/jstest.XXXXXX.js)
trap 'rm -f "$TMP"' EXIT

python3 - "$PAGE" "$TMP" <<'EOF'
import re, sys
t = open(sys.argv[1]).read()
scripts = re.findall(r'<script>(.*?)</script>', t, re.S)
if not scripts:
    sys.exit("jstest: no <script> block")
open(sys.argv[2], 'w').write("\n;\n".join(scripts))
EOF

node --check "$TMP"
echo "syntax ok: $PAGE"
node -e "
require('$TOOLS_DIR/dom_stub.js');
const m = require('$TMP');
if (m && typeof m.runAll === 'function') {
  const r = m.runAll();
  console.log('runAll:', r.pass, 'passed,', r.fail, 'failed');
  if (r.fail > 0) {
    for (const [e, res] of r.results)
      if (res && !res.pass) console.log('FAIL', e.title || '?', res.detail || '');
    process.exit(1);
  }
} else {
  console.log('loaded top-to-bottom with DOM stub (no runAll hook)');
}
"
