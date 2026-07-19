#!/bin/bash
# git-diff-staged.sh — print the staged diff for the pr-draft skill.
# Usage: bash scripts/git-diff-staged.sh
# If nothing is staged, prints nothing and exits 0 (caller decides fallback).

set -euo pipefail

# Require a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repository" >&2
  exit 1
fi

STAGED="$(git diff --cached --stat)"

if [ -z "$STAGED" ]; then
  echo "NOTE: nothing staged. Falling back to last commit's diff (HEAD~1..HEAD)." >&2
  git diff HEAD~1..HEAD
  exit 0
fi

# Print a summary + the full staged diff.
echo "=== Staged files ==="
echo "$STAGED"
echo
echo "=== Full staged diff ==="
git diff --cached
