const BASE = "/api";

async function post(body) {
  const res = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json();
}

export const api = {
  auditPortfolio: (username, max_repos = 5) =>
    post({ action: "audit-portfolio", username, max_repos }),
  apply: (jd, resume) => post({ action: "apply", jd, resume }),
  prDraft: (diff) => post({ action: "pr-draft", diff }),
  aiInfra: (question) => post({ action: "ai-infra-helper", question }),
  social: (idea, tone = "professional") => post({ action: "social", idea, tone }),
};
