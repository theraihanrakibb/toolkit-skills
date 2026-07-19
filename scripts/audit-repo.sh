#!/bin/bash
# audit-repo.sh — gather quality signals for a single repo.
# Used by the portfolio-audit skill. Outputs a simple key=value report
# that the skill (the model) interprets and scores against references/quality-bar.md.
#
# Usage: bash scripts/audit-repo.sh <path-to-repo>

set -euo pipefail

REPO="${1:-}"
if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
  echo "Usage: $0 <path-to-repo>" >&2
  exit 1
fi

cd "$REPO"

echo "repo_path=$REPO"
echo "repo_name=$(basename "$(pwd)")"

# File-existence checks (0 = missing, 1 = present)
check_file() {
  local pattern="$1"
  if ls $pattern 2>/dev/null | head -1 | grep -q .; then
    echo "$2=1"
  else
    echo "$2=0"
  fi
}

check_file "README*"        readme
check_file "LICENSE*"      license
check_file "CONTRIBUTING*" contributing
check_file "CODE_OF_CONDUCT*" code_of_conduct
check_file ".gitignore"    gitignore

# CI
if [ -d ".github/workflows" ] && ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | grep -q .; then
  echo "ci=1"
else
  echo "ci=0"
fi

# Tests directory or test files
if [ -d "tests" ] || [ -d "test" ]; then
  echo "tests=1"
elif ls test_*.py *_test.py *_test.go *.test.ts *.test.tsx *_spec.rb 2>/dev/null | head -1 | grep -q .; then
  echo "tests=1"
else
  echo "tests=0"
fi

# Examples
if [ -d "examples" ] || [ -d "example" ]; then
  echo "examples=1"
elif ls docs/quickstart.md 2>/dev/null | grep -q .; then
  echo "examples=1"
else
  echo "examples=0"
fi

# Releases / tags (skip for non-libraries; skill decides).
# Guard against non-git dirs (would exit non-zero under set -e + pipefail).
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  TAGS="$(git tag 2>/dev/null | wc -l | tr -d ' ')"
  echo "tags=$TAGS"
else
  echo "tags=0"
  echo "git_repo=0"
fi

# Repo description + topics (GitHub only, via gh CLI if available)
if command -v gh >/dev/null 2>&1 && git remote get-url origin >/dev/null 2>&1; then
  REMOTE="$(git remote get-url origin)"
  # Extract owner/repo from HTTPS or SSH URL
  SLUG="$(printf '%s' "$REMOTE" | sed -E 's#(https://github.com/|git@github.com:)##; s#\.git$##; s#^([^/]+/[^/]+).*$#\1#' | head -1)"
  if [ -n "$SLUG" ]; then
    DESC="$(gh repo view "$SLUG" --json description -q .description 2>/dev/null || echo "")"
    TOPICS="$(gh repo view "$SLUG" --json repositoryTopics -q '.repositoryTopics[].name' 2>/dev/null | tr '\n' ',' | sed 's/,$//')"
    [ -n "$DESC" ]   && echo "gh_description=$DESC"   || echo "gh_description="
    [ -n "$TOPICS" ] && echo "gh_topics=$TOPICS"     || echo "gh_topics="
  fi
fi

echo "audit_done=1"
