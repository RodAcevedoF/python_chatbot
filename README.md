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

---

# Documentación en Español (ES)

## Hotel Costa Azul — Chatbot

Chatbot ligero para Hotel Costa Azul. Proporciona un asistente potenciado por LLM que responde preguntas de los huéspedes usando la información del hotel y un vector store en Supabase para recuperación.

## Funcionalidades ✅

- API de chat (FastAPI) con LLM (GPT) y recuperación por vectores
- UI pulida servida desde `/ui/` (archivos estáticos)
- Herramienta de reindexado para subir la información del hotel a Supabase
- Límite de tasa, validación de entrada y protección de endpoints administrativos
- Endpoint de salud y `robots.txt` para seguridad en despliegue

## Inicio rápido (desarrollo) 🛠️

Requisitos: Python 3.11+, pip

1. Clona y crea entorno virtual

```bash
git clone <repo>
cd hotel_chatbot
python -m venv venv
# Windows
source venv/Scripts/activate
# macOS/Linux
# source venv/bin/activate
```

2. Instala dependencias

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` (NO LO COMPARTAS) y configura las variables:

```
SUPABASE_URL=
SUPABASE_KEY=
OPENAI_API_KEY=
ADMIN_API_KEY=
ALLOWED_ORIGINS=http://localhost:8000
```

4. Verifica el entorno

```bash
python cli.py check-env
```

5. Reindexa los datos del hotel (modo prueba)

```bash
python cli.py reindex --dry-run
```

6. Indexa de verdad (requiere claves de SUPABASE y OPENAI)

```bash
python cli.py reindex
```

7. Ejecuta la app localmente

```bash
python cli.py run-server
# o
uvicorn app.main:app --reload
```

Abre: http://127.0.0.1:8000/ (redirecciona a `/ui/index.html`)

## Endpoints de la API 📡

- POST `/chat` — endpoint principal de chat (JSON: { message, session_id })
- GET `/hotel-info` — devuelve la información del hotel
- POST `/reindex` — reindexa la información del hotel (administrador; requiere `x-api-key: ADMIN_API_KEY`)
- GET `/health` — health check para monitorización
- GET `/robots.txt` — reglas para buscadores (por defecto bloquea indexación)

## Despliegue (Render) 🚀

- `render.yaml` disponible para despliegue en un click
- Comando de build: `pip install -r requirements.txt`
- Comando de inicio recomendado:

```
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

- Configura las variables de entorno en el panel de Render (SUPABASE\_\*, OPENAI_API_KEY, ADMIN_API_KEY, ALLOWED_ORIGINS)
- Health check: `/health`

## Seguridad y buenas prácticas 🔐

- No subir `.env` ni secretos — usa Render secrets o un vault
- `/reindex` requiere `ADMIN_API_KEY` en el header; mantén la clave privada
- Se aplican límites de tasa y validación de entrada
- Usar HTTPS y configurar `ALLOWED_ORIGINS` en producción
- `robots.txt` bloquea rastreadores; ajusta si deseas indexación

## Mantenimiento y depuración 🧰

- Revisa logs: `docker-compose logs -f` o systemd/journalctl según corresponda
- Vuelve a ejecutar `python cli.py reindex` tras modificar `app/data/hotel_info.json`
- Monitoriza el uso de OpenAI y almacenamiento en Supabase

## Contribuciones

Las contribuciones son bienvenidas — abre issues o PRs.

## Licencia

MIT
