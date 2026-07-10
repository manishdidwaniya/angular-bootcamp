# AI Job Hunter

Executable monorepo for an AI-assisted job search and application-tracking platform.

## Applications

- `frontend/` — Angular 18, Tailwind CSS, Angular Material, signals, and lazy routes.
- `backend/` — FastAPI, SQLAlchemy async ORM, Pydantic, JWT authentication, and Alembic.
- `nginx/` — single public reverse proxy for the Angular application and `/api` routes.
- `docker-compose.yml` — PostgreSQL, Redis, backend, frontend, and Nginx.

## Run everything with Docker

Requirements: Docker Desktop with Linux containers enabled.

```bash
docker compose up --build
```

Open:

- Application: http://localhost
- Frontend directly: http://localhost:4200
- API documentation: http://localhost:8000/api/docs
- Health check: http://localhost:8000/health

The development backend creates missing database tables at startup. For production, set
`ENVIRONMENT=production` and run `alembic upgrade head` before starting the API.

## Run locally

Start the infrastructure from the repository root:

```bash
docker compose up -d postgres redis
```

Backend (Python 3.12+):

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (Node.js 20+), in another terminal:

```bash
cd frontend
npm ci
npm start
```

## Verification

```bash
# Backend
cd backend
python -m pytest -q

# Frontend production bundle
cd frontend
npm run build

# Validate Docker Compose
docker compose config
```

## Implemented API areas

- Registration, login, JWT refresh, and current-user access
- Authenticated profile creation, retrieval, and updates
- Job browsing and match-result contract
- Provider inventory
- Application tracking
- Notifications
- Dashboard analytics

The external provider collectors, scheduled ingestion, real AI matching, and outbound notification
adapters have extension points in the architecture but require provider credentials and later feature work.
