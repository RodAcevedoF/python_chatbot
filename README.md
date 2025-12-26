# Hotel Costa Azul — Chatbot

Lightweight chatbot for Hotel Costa Azul. Provides an LLM-powered assistant that answers guest questions using hotel data, supplemented by a Supabase vector store for retrieval.

## Features ✅

- Chat API (FastAPI) with LLM fallback (GPT) and vector retrieval
- Polished UI served from `/ui/` (static files)
- Re-indexing tooling to push hotel info into Supabase embeddings
- Rate limiting, input validation, and admin API key protection
- Health check and robots.txt for deployment safety

## Quick start (development) 🛠️

Prerequisites: Python 3.11+, pip

1. Clone and create virtual env

```bash
git clone <repo>
cd hotel_chatbot
python -m venv venv
# Windows
source venv/Scripts/activate
# macOS/Linux
# source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (DO NOT COMMIT) and set the required variables:

```
SUPABASE_URL=
SUPABASE_KEY=
OPENAI_API_KEY=
ADMIN_API_KEY=
ALLOWED_ORIGINS=http://localhost:8000
```

4. Verify environment

```bash
python cli.py check-env
```

5. Re-index the hotel data (dry-run)

```bash
python cli.py reindex --dry-run
```

6. Index for real (requires SUPABASE & OPENAI keys)

```bash
python cli.py reindex
```

7. Run the app locally

```bash
python cli.py run-server
# or
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/ (redirects to `/ui/index.html`)

## API endpoints 📡

- POST `/chat` — main chat endpoint (JSON: { message, session_id })
- GET `/hotel-info` — returns the hotel data
- POST `/reindex` — re-index hotel info (admin only; requires `x-api-key: ADMIN_API_KEY` header)
- GET `/health` — health check for monitoring
- GET `/robots.txt` — robots rules (blocks indexing by default)

## Deployment (Render) 🚀

- `render.yaml` is provided for one-click deploy
- Build command: `pip install -r requirements.txt`
- Start command (recommended):

```
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

- Set environment variables in Render Dashboard (SUPABASE\_\*, OPENAI_API_KEY, ADMIN_API_KEY, ALLOWED_ORIGINS)
- Health check path: `/health`

## Security & best practices 🔐

- Do not commit `.env` or secrets — use Render secrets or a vault
- `/reindex` requires `ADMIN_API_KEY` header; keep the key secret
- Rate limits and input validation are enabled to prevent abuse
- Use HTTPS and configure ALLOWED_ORIGINS in production
- robots.txt blocks crawlers by default; adjust if you want indexing

## Maintenance & debugging 🧰

- Check logs: `docker-compose logs -f` or systemd/journalctl as applicable
- Re-run `python cli.py reindex` after editing `app/data/hotel_info.json`
- Monitor OpenAI usage and Supabase storage

## Contributing

Contributions are welcome — please open issues or PRs.

## License

MIT
