# raihan-toolkit website

Full-stack web UI for the 5 CodeBuddy skills. FastAPI backend + React + Vite frontend. Template-based generation — no LLM dependency, works out of the box.

## Architecture

```
website/
├── backend/                # FastAPI app
│   ├── main.py             # /api/* endpoints
│   ├── skills.py           # template-based logic for 5 skills
│   ├── requirements.txt
│   └── README.md
└── frontend/               # React + Vite
    ├── package.json
    ├── vite.config.js       # /api proxied to localhost:8000
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx          # tabbed UI
        ├── api.js
        ├── style.css
        └── components/      # 5 components, one per skill
```

## Run locally (two terminals)

### Terminal 1 — backend
```bash
cd website/backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
OpenAPI docs at http://localhost:8000/docs.

### Terminal 2 — frontend
```bash
cd website/frontend
npm install
npm run dev
```
App at http://localhost:5173. The Vite dev server proxies `/api/*` to the FastAPI backend.

## Skills → endpoints

| Skill | Endpoint | Frontend tab |
|---|---|---|
| Portfolio audit | `POST /api/audit-portfolio` | Portfolio Audit |
| Job application | `POST /api/apply` | Job Application |
| PR draft | `POST /api/pr-draft` | PR Draft |
| AI-infra helper | `POST /api/ai-infra-helper` | AI-Infra Helper |
| Social media | `POST /api/social` | Social Media |

## Notes

- `audit-portfolio` hits the GitHub API (unauthenticated = 60 req/hr per IP). Set `GITHUB_TOKEN` for higher limits.
- All generation is template-based. To plug in a real LLM, replace functions in `backend/skills.py` with calls to an OpenAI-compatible endpoint.
- **No AI-generation footers** in any output (per the plugin's hard rule). The PR-draft endpoint emits `No AI-generation footer.` explicitly.

## Deployment (optional, later)

- Backend: any Python host (Fly.io, Railway, Render). Set `GITHUB_TOKEN` env var.
- Frontend: build with `npm run build`, deploy `dist/` to Vercel / Netlify / GitHub Pages. Point the frontend at the backend URL by editing `src/api.js` (`BASE` constant).
