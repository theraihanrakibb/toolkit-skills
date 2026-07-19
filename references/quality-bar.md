# The 10/10 Quality Bar

Reference for the `portfolio-audit` skill. Each criterion scored 0 or 1 (or 0/0.5/1 for partial). Total = sum, max 10. A repo is "job-hunt ready" at ≥ 9.

## Criteria (10 items × 1 point)

1. **README exists and is high quality**
   - Has a one-line description at the top.
   - Has install/run/usage sections with code blocks.
   - Has at least one of: screenshot, example, demo link, architecture diagram.
   - 0 = missing, 0.5 = stub, 1 = solid.

2. **LICENSE present** — must be a real SPDX file (MIT, Apache-2.0, BSD-3, etc.).

3. **CI present** — `.github/workflows/*.yml` with at least lint or test on push/PR.

4. **Tests present** — `tests/`, `test/`, `*_test.py`, `*.test.ts(x)`, `*_spec.rb`, etc. Non-trivial (≥ 3 tests).

5. **Examples directory** — `examples/` with at least one runnable sample, OR a `docs/quickstart.md`.

6. **CONTRIBUTING.md** — how to contribute, dev setup, PR conventions.

7. **CODE_OF_CONDUCT.md** — Contributor Covenant or equivalent.

8. **.gitignore appropriate for the language** — Python: `__pycache__/`, `.venv/`, `*.pyc`; Node: `node_modules/`; etc. No junk committed.

9. **Repo description + topics on GitHub** — `gh repo edit --description "..." --add-topic topic1,topic2`. At least 3 topics.

10. **Releases or tags** (for libraries/tools) — at least one semver tag or GitHub Release with notes. Skip this criterion for non-library repos (score out of 9 instead of 10).

## Scoring output format

```markdown
| Repo | Score | README | LICENSE | CI | Tests | Examples | CONTRIBUTING | CoC | .gitignore | Desc+Topics | Releases |
|---|---|---|---|---|---|---|---|---|---|---|---|
| foo | 8/10 | 1 | 1 | 1 | 0.5 | 0 | 0 | 1 | 1 | 1 | 1 |
```

## Fix-plan priority
1. `[easy]` Add LICENSE, .gitignore, repo description+topics (≤ 5 min each, no code).
2. `[easy]` Scaffold a basic README if missing.
3. `[medium]` Add CONTRIBUTING.md + CODE_OF_CONDUCT.md.
4. `[medium]` Add a minimal CI workflow (lint only is fine for v1).
5. `[hard]` Add tests + examples — requires real engineering work.
