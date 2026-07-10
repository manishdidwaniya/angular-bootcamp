# AI Job Hunter

Executable monorepo for a freshness-first, profile-aware job search and application tracker.

## Applications

- `frontend/` — Angular 21 LTS, Tailwind CSS, signals, and lazy routes.
- `backend/` — FastAPI, async SQLAlchemy, Pydantic, JWT authentication, Alembic, and scheduled ingestion.
- `nginx/` — one public reverse proxy for the Angular application and `/api` routes.
- `docker-compose.yml` — PostgreSQL, Redis, backend, frontend, and Nginx.

## Run everything with Docker

Requirements: Docker Desktop with Linux containers enabled.

```bash
docker compose up --build
```

Open the application at `http://localhost`, the frontend directly at `http://localhost:4200`,
or API docs at `http://localhost:8000/api/docs`.

## Run locally

Start PostgreSQL and Redis from the repository root:

```bash
docker compose up -d postgres redis
```

Backend (Python 3.12+):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend (Node.js 20+), in another terminal:

```powershell
cd frontend
npm ci
npm start
```

Open `http://localhost:4200`, register, and complete these steps:

1. Add target roles and skills under **Profiles**.
2. Add text resumes under **Resumes** for resume-fit suggestions.
3. Set freshness and notification preferences under **Settings**.
4. Open **Jobs** and choose **Sync latest jobs**. Recommended jobs are the default view.

Arbeitnow, We Work Remotely, and The Muse work without credentials. Adzuna is enabled when
`ADZUNA_APP_ID` and `ADZUNA_APP_KEY` are present in `backend/.env`. Copy `.env.example` to `.env`
and add optional SMTP, Telegram, Slack, or Discord values only when those channels are needed.

## Freshness and accuracy guarantees

- Every accepted job must have a real source posting timestamp.
- Future-dated jobs and jobs older than the selected 1–30 day window are rejected.
- Expired or stale records are marked inactive and excluded from every result.
- Jobs are newest-first and deduplicated by source ID and a normalized title/company/location fingerprint.
- Recommendations apply profile, search, and location criteria and exclude matches below 45% by default.
- The scheduler refreshes providers every 30 minutes by default; both values are configurable in `.env`.
- Only official/public provider APIs and RSS feeds are used; LinkedIn and Indeed are not scraped.

## Verification

```powershell
cd backend
.\.venv\Scripts\ruff.exe check app
.\.venv\Scripts\mypy.exe app
.\.venv\Scripts\pytest.exe -q

cd ..\frontend
npm run lint
npm run build

cd ..
docker compose config
```

## Implemented areas

- Registration, login, JWT refresh, and current-user access
- Career profile, target-role, skill, company, and resume management
- Live Arbeitnow, We Work Remotely, The Muse, and optional Adzuna ingestion
- Timestamp validation, freshness cutoffs, deduplication, and source health
- Explainable profile/resume matching and newest-first recommendations
- Application tracking with pipeline status updates
- In-app and optional SMTP, Telegram, Slack, and Discord notifications
- Dashboard analytics and scheduled refresh
