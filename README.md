
# 🧬 Oncology AI Agent
### Evidence-Based Mutation-to-Therapy Recommendation System

---

## Run locally

Start the backend API:

```bash
python -m pip install -e .
uvicorn app.api.main:app --reload --port 8000
```

Start the frontend (in a separate terminal):

```bash
cd app/frontend
npm install
npm run dev
```

Frontend expects the backend at `http://localhost:8000/api` by default (see `app/frontend/.env`).


## 📌 Project Overview

The Oncology AI Agent is a clinical decision-support prototype designed to map gene mutations and cancer types to evidence-backed targeted therapies.

The system uses a deterministic rule engine for therapy selection and an optional LLM-based explanation layer for generating human-readable summaries.

⚠️ **Disclaimer:** This system is developed for research and educational purposes only. It does not provide medical advice and must not be used for clinical decision-making.

---
