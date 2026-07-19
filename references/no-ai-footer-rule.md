# The No-AI-Footer Rule (HARD)

**No AI-generation footers anywhere in this plugin's output.**

## What counts as a footer
- `Generated with CodeBuddy Code`
- `Generated with Claude Code`
- `Co-Authored-By: Claude <noreply@anthropic.com>`
- `Co-Authored-By: Copilot <noreply@github.com>`
- `🤖 Generated with ...`
- Any trailer attributing the work to an AI tool.

## Why
- The user maintains job-hunt and public repos. AI footers on commits/PRs:
  - look unprofessional to recruiters reviewing commit history,
  - reveal tooling choice on public repos where the user prefers neutrality,
  - get parsed by GitHub as a co-author (e.g. the `claude` bot appears as a contributor — visually polluting the contributor list).
- This is a strong user preference, confirmed via feedback memory: "omit 'Generated with...' trailers on job-hunt/public repos."

## Where it's enforced
1. **Each SKILL.md** — instructs the model never to emit footers.
2. **`hooks/validate-commit.sh`** — a PreToolUse hook on Bash that DENIES `git commit` calls whose message contains AI-footer patterns. Suggests a clean Conventional Commit message instead.

## How to write a clean commit message
```
<type>(<scope>): <subject>

<body explaining why, not what>
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`.
- **Subject:** ≤ 72 chars, imperative mood, lowercase first word, no trailing period.
- **Body:** wrap at 72 chars, explain motivation.
- **No trailers** unless it's a `Signed-off-by` for repos that require DCO.

## How to write a clean PR description
Use `templates/pr-description.md`. Sections: Summary, Changes, Why, Testing, Screenshots. No footers.

## How to write a clean cover letter / social post
Just write the content. No "— Generated with CodeBuddy" sign-off. No "Co-authored by AI" note anywhere.
