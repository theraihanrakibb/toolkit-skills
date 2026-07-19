import { useState } from "react";
import SocialMedia from "./components/SocialMedia.jsx";
import PrDraft from "./components/PrDraft.jsx";
import AuditPortfolio from "./components/AuditPortfolio.jsx";
import Apply from "./components/Apply.jsx";
import AiInfra from "./components/AiInfra.jsx";

const TABS = [
  { id: "social", label: "Social Media", component: SocialMedia },
  { id: "pr-draft", label: "PR Draft", component: PrDraft },
  { id: "audit", label: "Portfolio Audit", component: AuditPortfolio },
  { id: "apply", label: "Job Application", component: Apply },
  { id: "ai-infra", label: "AI-Infra Helper", component: AiInfra },
];

export default function App() {
  const [active, setActive] = useState("social");
  const ActiveComponent = TABS.find((t) => t.id === active).component;

  return (
    <div className="app">
      <h1>raihan-toolkit</h1>
      <p className="subtitle">
        Web UI for the 5 skills: audit-portfolio, apply, pr-draft, ai-infra-helper, social.
        Backend runs on <code>localhost:8000</code>.
      </p>
      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`tab ${active === t.id ? "active" : ""}`}
            onClick={() => setActive(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>
      <ActiveComponent />
    </div>
  );
}
