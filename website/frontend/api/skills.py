"""Skill logic for the Toolkit Skills Vercel serverless function.

Ported from website/backend/skills.py. Uses only the standard library so the
function has zero pip dependencies (fast cold starts, no requirements.txt).
"""

import json
import re
import urllib.error
import urllib.request

GITHUB_API = "https://api.github.com"


def _github_get(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "toolkit-skills"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# 1. Portfolio audit
# ---------------------------------------------------------------------------
def audit_portfolio(username, max_repos=5, token=None):
    """Score a GitHub user's top repos against a 10-point quality bar."""
    try:
        repos = _github_get(
            f"{GITHUB_API}/users/{username}/repos?per_page=100&sort=pushed", token
        )
    except urllib.error.HTTPError as e:
        return {"error": f"GitHub API {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}"}
    except Exception as e:  # noqa: BLE001
        return {"error": f"GitHub request failed: {e}"}

    if not isinstance(repos, list):
        return {"error": "Unexpected GitHub response."}

    repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:max_repos]

    scored = []
    for repo in repos:
        full_name = repo.get("full_name", repo.get("name", "?"))
        readme_ok = True  # assume present; cheap heuristic for the demo
        try:
            _github_get(f"{GITHUB_API}/repos/{full_name}/readme", token)
            readme_ok = True
        except Exception:  # noqa: BLE001
            readme_ok = False
        license_ok = bool(repo.get("license"))
        topics = repo.get("topics", []) or []
        description = repo.get("description") or ""
        has_pages = bool(repo.get("has_pages"))
        has_issues = bool(repo.get("has_issues"))
        archived = bool(repo.get("archived"))
        forks = repo.get("forks_count", 0)
        stars = repo.get("stargazers_count", 0)
        homepage = repo.get("homepage") or ""

        score = 1 if readme_ok else 0
        score += 1 if license_ok else 0
        score += 1 if topics else 0
        score += 1 if description else 0
        score += 1 if has_pages else 0
        score += 1 if has_issues else 0
        score += 1 if forks > 0 else 0
        score += 1 if stars > 0 else 0
        score += 1 if not archived else 0
        score += 1 if homepage else 0

        scored.append({
            "name": full_name,
            "stars": stars,
            "forks": forks,
            "description": description,
            "topics": topics,
            "license": repo.get("license", {}).get("spdx_id") if repo.get("license") else None,
            "has_readme": readme_ok,
            "has_pages": has_pages,
            "score": score,
            "max_score": 10,
            "fix_plan": _fix_plan(readme_ok, license_ok, topics, description, has_pages),
        })

    return {"username": username, "repos": scored}


def _fix_plan(readme_ok, license_ok, topics, description, pages):
    plan = []
    if not readme_ok:
        plan.append("[easy] Add a README.md")
    if not license_ok:
        plan.append("[easy] Add a LICENSE file (MIT recommended)")
    if not topics:
        plan.append("[easy] Add 3-5 topics via gh repo edit --add-topic")
    if not description:
        plan.append("[easy] Set a repo description")
    if not pages:
        plan.append("[medium] Enable GitHub Pages for a project site")
    if not plan:
        plan.append("[ok] All easy items satisfied - focus on tests + CI next.")
    return plan


# ---------------------------------------------------------------------------
# 2. Job application
# ---------------------------------------------------------------------------
def apply(jd, resume):
    jd_keywords = _extract_keywords(jd or "")
    resume_keywords = _extract_keywords(resume or "")
    resume_set = {r.lower() for r in resume_keywords}
    matched = [k for k in jd_keywords if k.lower() in resume_set]
    missing = [k for k in jd_keywords if k.lower() not in resume_set][:8]

    m = re.search(r"\b(?:at|join)\s+([A-Z][A-Za-z0-9&]+(?:\s+[A-Z][A-Za-z0-9&]+)*)", jd or "")
    company = m.group(1).strip() if m else "your company"
    m = re.search(r"\b(Engineer|Developer|Intern|Lead|Architect|Scientist)[A-Za-z ]{0,30}", jd or "")
    role = m.group(0).strip() if m else "the role"

    cover_letter = (
        f"Dear Hiring Team at {company},\n\n"
        f"I'm writing to apply for {role}. The job description emphasizes "
        f"{', '.join(jd_keywords[:3])}, which aligns directly with my background.\n\n"
        f"In my recent work, I have focused on {', '.join(matched[:3]) or 'building production systems'}, "
        f"with attention to reliability and measurable impact. I'm confident I can contribute to "
        f"{company}'s goals from day one.\n\n"
        f"I'm especially drawn to {company} because of its engineering culture and the problems the "
        f"team is solving. I'd welcome the chance to discuss how my experience maps to your needs.\n\n"
        f"Thank you for your time and consideration.\n\nBest regards,\n[Your Name]\n"
    )

    interview_questions = (
        [f"Walk me through a project where you used {k}." for k in matched[:3]]
        + [
            "Tell me about a time you debugged a hard issue under pressure.",
            "How do you approach writing tests for a new feature?",
            "Describe a system you designed end-to-end.",
            "What's a trade-off you made recently, and why?",
        ]
        + [f"How would you ramp up on {k} if you haven't used it?" for k in missing[:3]]
    )

    skills_gap = [{"skill": k, "status": "learnable-quickly" if len(k) < 12 else "stretch"} for k in missing]

    prep_plan = [
        "Day 1: Re-read the JD; map each requirement to a resume bullet or a project you'll lean on.",
        "Day 2: Practice a 90-second intro (who you are, what you've built, why this role).",
        "Day 3: Drill 3 technical questions on the matched skills.",
        "Day 4: Prepare 2 stories using STAR (one challenge, one collaboration).",
        "Day 5: Study one missing skill - enough to talk about it for 2 minutes.",
        "Day 6: Mock interview (with a friend or in front of a camera).",
        "Day 7: Rest, prepare questions for them, confirm logistics.",
    ]

    return {
        "company": company,
        "role": role,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "cover_letter": cover_letter,
        "interview_questions": interview_questions,
        "skills_gap": skills_gap,
        "prep_plan": prep_plan,
    }


def _extract_keywords(text):
    stopwords = {"the", "and", "for", "with", "you", "our", "will", "this", "that", "from", "have", "are"}
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+#.]{2,}", text or "")
    seen, out = set(), []
    for t in tokens:
        low = t.lower()
        if low in stopwords or low in seen:
            continue
        seen.add(low)
        out.append(t)
    return out[:12]


# ---------------------------------------------------------------------------
# 3. PR draft
# ---------------------------------------------------------------------------
def pr_draft(diff):
    files = re.findall(r"^\+\+\+ b/(.+)$", diff or "", flags=re.MULTILINE)
    additions = len(re.findall(r"\n\+", diff or ""))
    deletions = len(re.findall(r"\n-", diff or ""))

    joined = " ".join(files).lower()
    if any(k in joined for k in ["readme", "doc", "license", ".md"]):
        ctype = "docs"
    elif any(k in joined for k in ["test", "spec"]):
        ctype = "test"
    elif any(k in joined for k in [".yml", ".yaml", "github/workflows", "dockerfile"]):
        ctype = "ci"
    elif any(k in joined for k in ["refactor", "rename"]):
        ctype = "refactor"
    else:
        ctype = "feat"

    scope = files[0].split("/")[0] if files else "core"
    subject = f"update {scope}" if files else "update project"

    commit_message = f"{ctype}({scope}): {subject}\n\nUpdates {len(files)} file(s). +{additions} -{deletions}."
    pr_description = (
        f"## Summary\nUpdates {len(files)} file(s) across `{scope}`.\n\n"
        f"## Changes\n" + "\n".join(f"- `{f}`" for f in files) + f"\n\n"
        f"## Why\n[Explain the motivation here.]\n\n"
        f"## Testing\n- [ ] `pre-commit run --all-files` is green\n- [ ] Targeted test passes locally\n\n"
        f"## Stats\n+{additions} additions / -{deletions} deletions across {len(files)} file(s).\n"
    )
    changelog = f"- [{ctype}] {scope}: {subject}"

    return {
        "commit_message": commit_message,
        "pr_description": pr_description,
        "changelog_entry": changelog,
        "files": files,
        "additions": additions,
        "deletions": deletions,
    }


# ---------------------------------------------------------------------------
# 4. AI-infra helper
# ---------------------------------------------------------------------------
def ai_infra_helper(question):
    q = (question or "").lower()
    if "sglang" in q or ("model" in q and "add" in q):
        return {
            "repo": "sglang",
            "layout": {
                "models": "python/sglang/srt/models/<arch>.py",
                "scheduler": "python/sglang/srt/managers/scheduler.py",
                "server": "python/sglang/srt/entrypoints/",
                "frontend": "python/sglang/lang/",
                "tests": "test/srt/",
            },
            "commands": [
                "pre-commit install && pre-commit run --all-files",
                "pytest test/srt/test_<area>.py -k <name> -x",
            ],
            "ci_behavior": "Fork PRs fail pr-gate / pr-test-* by design (need repo secrets). Only `lint` actually gates your code. Make lint green; don't chase pr-test-*.",
            "answer": f"For '{question}': see SGLang layout above. Likely file: python/sglang/srt/models/<arch>.py",
        }
    if "vllm" in q:
        return {
            "repo": "vllm",
            "layout": {
                "models": "vllm/model_executor/models/",
                "engine": "vllm/engine/",
                "entrypoints": "vllm/entrypoints/",
                "tests": "tests/",
            },
            "commands": ["./.format.sh", "pytest tests/<area>/test_x.py -k <name> -x"],
            "ci_behavior": "Similar to SGLang: fork PRs can't access GPU CI. Make ruff + black green.",
            "answer": f"For '{question}': see vLLM layout above.",
        }
    return {
        "repo": "generic",
        "answer": f"Question '{question}' doesn't match SGLang or vLLM. Try asking about 'sglang', 'vllm', 'where to add a model', or 'what tests to run'.",
    }


# ---------------------------------------------------------------------------
# 5. Social media
# ---------------------------------------------------------------------------
def social(idea, tone="professional"):
    hook = (idea or "")[:120]
    facebook = f"{hook}\n\nWhat do you think? Drop a comment below. 👇"
    instagram = (
        f"{hook}\n\nSave this for later 🔖 and share with someone who needs to see it.\n\n"
        f"#ai #buildinpublic #developer #tech #programming"
    )
    youtube_title = (idea or "")[:90]
    youtube_description = (
        f"{hook}\n\nIn this video we break down the idea, walk through the implementation, and "
        f"show concrete results.\n\n0:00 Intro\n0:30 Context\n1:15 Demo\n3:00 Takeaways\n\n"
        f"Links: [placeholder]\n\nTags: ai, programming, buildinpublic, developer, tech, tutorial, howto"
    )
    tweet = (idea or "")[:277] + ("…" if len(idea or "") > 277 else "")
    linkedin = (
        f"{hook}\n\nI've been thinking about this, and here's my take:\n\n"
        f"- It's easy to overlook the small things.\n- The compounding effect is real.\n"
        f"- Sharing what you learn helps everyone.\n\nWhat's your experience with this? Curious to hear from the network."
    )
    gmail_subject = (idea or "")[:55]
    gmail_body = (
        f"Hi [Name],\n\n{hook}\n\nI thought this might be relevant given what you're working on. "
        f"Happy to share more detail if useful.\n\nBest,\n[Your Name]"
    )
    return {
        "idea": idea,
        "tone": tone,
        "platforms": {
            "facebook": facebook,
            "instagram": instagram,
            "youtube_title": youtube_title,
            "youtube_description": youtube_description,
            "youtube_tags": ["ai", "programming", "buildinpublic", "developer", "tech", "tutorial", "howto"],
            "twitter": tweet,
            "linkedin": linkedin,
            "gmail_subject": gmail_subject,
            "gmail_body": gmail_body,
        },
        "hashtags": ["#ai", "#buildinpublic", "#developer", "#tech", "#programming", "#coding"],
    }


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
def dispatch(action, body):
    if action == "audit-portfolio":
        return audit_portfolio(body.get("username", ""), body.get("max_repos", 5),
                               token=_env_token())
    if action == "apply":
        return apply(body.get("jd", ""), body.get("resume", ""))
    if action == "pr-draft":
        return pr_draft(body.get("diff", ""))
    if action == "ai-infra-helper":
        return ai_infra_helper(body.get("question", ""))
    if action == "social":
        return social(body.get("idea", ""), body.get("tone", "professional"))
    raise ValueError(f"unknown action: {action}")


def _env_token():
    import os
    return os.getenv("GITHUB_TOKEN")
