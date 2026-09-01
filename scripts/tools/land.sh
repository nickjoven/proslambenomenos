#!/usr/bin/env bash
# land.sh - the landing pipeline as one command, one digest line.
#
# Usage (from inside a task worktree, on its branch):
#   scripts/tools/land.sh "<pr title>" <commit-msg-file> [pr-body-file]
#
# Runs: stage everything -> commit (message from file) -> make gates
# -> message gate -> push -> gh pr create -> CI wait -> rebase-merge
# -> sync the main checkout -> wt-done -> repack. Prints a DIGEST
# block and nothing else on success. Any failing step stops the
# pipeline with that step's output.
#
# The commit message and PR prose stay the caller's job - this
# script owns only the replayable mechanics.
set -euo pipefail

TITLE=${1:?usage: land.sh "<pr title>" <commit-msg-file> [pr-body-file]}
MSGFILE=${2:?commit message file required}
BODYFILE=${3:-}

WT=$(git rev-parse --show-toplevel)
cd "$WT"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TASK=${BRANCH}
MAIN=~/code/proslambenomenos
[ "$WT" = "$(cd $MAIN && pwd)" ] && {
  echo "land.sh: refusing to run in the main checkout" >&2; exit 2; }

git add -A
if ! git diff --cached --quiet; then
  git commit -q -F "$MSGFILE"
fi

# capture, then grep: piping make into grep -q dies of SIGPIPE
# under pipefail when invoked from a parent make (dogfood run 2);
# clearing MAKEFLAGS keeps the sub-make independent of the parent
GATES_OUT=$(MAKEFLAGS= MAKELEVEL= make gates 2>&1) || true
echo "$GATES_OUT" | grep -q "worst rc: 0" || {
  echo "land.sh: gates red" >&2
  echo "$GATES_OUT" | tail -20; exit 1; }
python3 scripts/check_messages.py origin/main..HEAD

git push -q -u origin "$BRANCH"
if [ -n "$BODYFILE" ]; then
  PR_URL=$(gh pr create --title "$TITLE" --body-file "$BODYFILE" 2>&1 | tail -1)
else
  PR_URL=$(gh pr create --title "$TITLE" --body "$(printf '%s\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)' "$TITLE")" 2>&1 | tail -1)
fi
PR_NUM=${PR_URL##*/}

until gh pr checks "$PR_NUM" 2>/dev/null | grep -qE 'pass|fail'; do
  sleep 20
done
CI=$(gh pr checks "$PR_NUM" | head -1)
echo "$CI" | grep -q pass || {
  echo "land.sh: CI failed on PR $PR_NUM" >&2
  gh pr checks "$PR_NUM"; exit 1; }

gh pr merge "$PR_NUM" --rebase
cd "$MAIN"
git fetch -q origin && git merge -q --ff-only origin/main
NEW_MAIN=$(git log --oneline -1)
make wt-done TASK="$TASK" >/dev/null 2>&1 || true
make handoff >/dev/null 2>&1 || true
CID=$(head -c 16 ~/code/handoffs/LAST_CID 2>/dev/null || echo "?")

echo "DIGEST"
echo "  pr:     #$PR_NUM merged ($PR_URL)"
echo "  ci:     $CI"
echo "  main:   $NEW_MAIN"
echo "  packet: $CID"
