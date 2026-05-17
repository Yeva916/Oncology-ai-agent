# Backend (FastAPI)

Run the backend API (requires Python 3.11+). From the repository root:

```bash
python -m pip install -e .
uvicorn app.api.main:app --reload --port 8000
```

This exposes the API under `http://localhost:8000/api` with endpoints:
- `POST /api/analyze` (JSON: `{ "query": "...", "context": [...] }`)
- `GET /api/demo`
- `GET /api/health`

Ensure `GOOGLE_API_KEY` and other credentials are set in `.env` if you want the demo/analyze flows to call external LLMs.
