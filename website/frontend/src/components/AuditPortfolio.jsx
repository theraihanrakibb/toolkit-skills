import { useState } from "react";
import { api } from "../api.js";

function scoreClass(score) {
  if (score >= 8) return "good";
  if (score >= 5) return "mid";
  return "low";
}

export default function AuditPortfolio() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const run = async () => {
    if (!username.trim()) { setError("Enter a GitHub username."); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api.auditPortfolio(username.trim()));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Audit a GitHub portfolio</h2>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        Scores a user's top 5 public repos against a 10-point quality bar (README, LICENSE, topics, description, pages, issues, forks, stars, not-archived, homepage).
      </p>

      <label>GitHub username</label>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="e.g. theraihanrakibb" />

      <button className="primary" onClick={run} disabled={loading}>
        {loading ? "Auditing…" : "Audit portfolio"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          {result.error ? (
            <div className="error">{result.error}</div>
          ) : (
            <>
              <h3>{result.username} — {result.repos.length} repos</h3>
              <table>
                <thead>
                  <tr><th>Repo</th><th>Score</th><th>Stars</th><th>License</th><th>Readme</th></tr>
                </thead>
                <tbody>
                  {result.repos.map((r) => (
                    <tr key={r.name}>
                      <td>{r.name}</td>
                      <td><span className={`score ${scoreClass(r.score)}`}>{r.score}/10</span></td>
                      <td>{r.stars}</td>
                      <td>{r.license || "—"}</td>
                      <td>{r.has_readme ? "yes" : "no"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {result.repos.map((r) => (
                <div key={r.name} style={{ marginTop: 16 }}>
                  <h4>{r.name}</h4>
                  <p style={{ color: "var(--muted)", fontSize: "0.85rem" }}>{r.description || "no description"}</p>
                  <ul>
                    {r.fix_plan.map((p, i) => <li key={i} style={{ fontSize: "0.85rem" }}>{p}</li>)}
                  </ul>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
