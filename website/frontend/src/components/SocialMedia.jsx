import { useState } from "react";
import { api } from "../api.js";

export default function SocialMedia() {
  const [idea, setIdea] = useState("");
  const [tone, setTone] = useState("professional");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const run = async () => {
    if (!idea.trim()) { setError("Enter an idea first."); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api.social(idea, tone));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Draft social content</h2>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        One idea → 6 platform drafts (Facebook, Instagram, YouTube, X, LinkedIn, Gmail). Template-based, no auto-posting.
      </p>

      <label>Content idea</label>
      <textarea value={idea} onChange={(e) => setIdea(e.target.value)} placeholder="e.g. I just shipped a FastAPI gateway with rate limiting and cost caps" />

      <label>Tone</label>
      <select value={tone} onChange={(e) => setTone(e.target.value)}>
        <option value="professional">professional</option>
        <option value="casual">casual</option>
        <option value="promotional">promotional</option>
        <option value="educational">educational</option>
      </select>

      <button className="primary" onClick={run} disabled={loading}>
        {loading ? "Drafting…" : "Draft for all 6 platforms"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Drafts</h3>
          <ul className="platforms">
            <li><h4>Facebook</h4><pre>{result.platforms.facebook}</pre></li>
            <li><h4>Instagram</h4><pre>{result.platforms.instagram}</pre></li>
            <li><h4>YouTube title</h4><pre>{result.platforms.youtube_title}</pre></li>
            <li><h4>YouTube description</h4><pre>{result.platforms.youtube_description}</pre></li>
            <li><h4>X / Twitter</h4><pre>{result.platforms.twitter}</pre></li>
            <li><h4>LinkedIn</h4><pre>{result.platforms.linkedin}</pre></li>
            <li><h4>Gmail subject</h4><pre>{result.platforms.gmail_subject}</pre></li>
            <li><h4>Gmail body</h4><pre>{result.platforms.gmail_body}</pre></li>
          </ul>
          <p style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
            Hashtags: {result.hashtags.join(", ")}
          </p>
        </div>
      )}
    </div>
  );
}
