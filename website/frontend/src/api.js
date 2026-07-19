const BASE = "/api";

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
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
    post("/audit-portfolio", { username, max_repos }),
  apply: (jd, resume) => post("/apply", { jd, resume }),
  prDraft: (diff) => post("/pr-draft", { diff }),
  aiInfra: (question) => post("/ai-infra-helper", { question }),
  social: (idea, tone = "professional") => post("/social", { idea, tone }),
};
