import { useState } from "react";
import { api } from "../api.js";

export default function AiInfra() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const run = async () => {
    if (!question.trim()) { setError("Ask a question."); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api.aiInfra(question));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>AI-infra contributor helper</h2>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        Ask about navigating SGLang / vLLM. Returns repo layout, test/lint commands, and the fork-PR CI behavior.
      </p>

      <label>Question</label>
      <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="e.g. where do I add a new model in sglang?" />
      <p style={{ color: "var(--muted)", fontSize: "0.8rem" }}>Try: "sglang add model", "vllm tests", "why is my fork PR CI failing"</p>

      <button className="primary" onClick={run} disabled={loading}>
        {loading ? "Looking up…" : "Get guidance"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>{result.repo}</h3>
          <p>{result.answer}</p>

          {result.layout && (
            <>
              <h4>Layout</h4>
              <pre>{Object.entries(result.layout).map(([k, v]) => `${k}: ${v}`).join("\n")}</pre>
            </>
          )}

          {result.commands && (
            <>
              <h4>Commands</h4>
              <pre>{result.commands.join("\n")}</pre>
            </>
          )}

          {result.ci_behavior && (
            <>
              <h4>CI behavior</h4>
              <p style={{ color: "var(--warn)", fontSize: "0.9rem" }}>{result.ci_behavior}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
