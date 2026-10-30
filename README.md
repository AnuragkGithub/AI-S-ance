# 👻 Repo Séance

**The past left code. We bring it back to life.**

Repo Séance is a local-first, open-weight AI software archaeology assistant. Import a public GitHub repository or ZIP archive, inspect its structure, ask questions grounded in retrieved source files, and generate a repository resurrection report.

> Competition/demo project. The current version performs static inspection and keyword-based evidence retrieval, then uses a locally running Ollama model to formulate answers. It does not execute imported project code.

## Features

- Import public GitHub repositories or ZIP archives.
- Static source-file indexing with common generated/vendor folders excluded.
- Language and repository statistics.
- Evidence-grounded chat using retrieved source chunks and file/line references.
- Browse indexed source files.
- Download a Markdown resurrection report.
- Local Ollama inference; no proprietary AI API is required.
- Responsive dark developer interface.
- Docker Compose setup for the app and Ollama.

## Architecture

```text
Browser (responsive HTML/CSS/JS)
              |
              v
        FastAPI application
              |
     +--------+---------+
     |                  |
     v                  v
Repository scanner   SQLite index
     |                  |
     +------ chunks ----+
              |
              v
    Evidence retrieval (local)
              |
              v
       Ollama / open model
              |
              v
  Answer + source references
```

The first release intentionally keeps retrieval lightweight and dependable. It uses local lexical ranking rather than requiring a separate vector database or embedding service. A semantic embedding index is a planned extension, not a claimed current feature.

## Requirements

- Python 3.10+
- Git CLI (for GitHub URL import)
- Ollama installed and running
- A model supported by your machine

## Quick start (local)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/repo-seance.git
cd repo-seance
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r backend/requirements.txt
```

### 3. Install and start Ollama

Install Ollama from https://ollama.com/download, then run:

```bash
ollama pull qwen2.5-coder:7b
ollama serve
```

The 7B model needs sufficient memory. If your computer cannot run it, select a smaller model available in Ollama and set `OLLAMA_MODEL` accordingly. Model quality and speed depend on hardware.

### 4. Start Repo Séance

In another terminal, from the project root:

```bash
# macOS / Linux
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5-coder:7b
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Windows PowerShell:

```powershell
$env:OLLAMA_BASE_URL="http://localhost:11434"
$env:OLLAMA_MODEL="qwen2.5-coder:7b"
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000.

## Docker Compose (local full stack)

```bash
docker compose up --build -d
# Pull the model inside the Ollama container
docker compose exec ollama ollama pull qwen2.5-coder:7b
```

Open http://localhost:8000. First model download can be several GB. Keep the Docker volumes so model files and repository data persist.

To inspect logs:

```bash
docker compose logs -f app
docker compose logs -f ollama
```

## API

- `GET /api/health` — application and Ollama status
- `GET /api/repositories` — list indexed repositories
- `POST /api/repositories/clone` — JSON `{ "url": "https://github.com/owner/repo" }`
- `POST /api/repositories/upload` — multipart ZIP upload (`file`)
- `GET /api/repositories/{id}` — repository metadata
- `GET /api/repositories/{id}/autopsy` — static analysis summary
- `GET /api/repositories/{id}/files` — indexed source file list
- `GET /api/repositories/{id}/file?path=...` — read an indexed text file
- `POST /api/repositories/{id}/chat` — JSON `{ "question": "Explain the app entry point" }`
- `GET /api/repositories/{id}/report` — download Markdown report
- `DELETE /api/repositories/{id}` — delete repository and index

Interactive API docs: http://localhost:8000/docs.

## Deploying a public demo

The application container can be deployed to a Docker-capable host, but **the app container alone does not provide an AI model**. Configure a reachable Ollama-compatible inference service and set:

- `APP_ROOT=/app`
- `DATA_DIR=/data` (attach persistent storage)
- `OLLAMA_BASE_URL=https://YOUR-PRIVATE-OLLAMA-ENDPOINT`
- `OLLAMA_MODEL=qwen2.5-coder:7b`
- `MAX_UPLOAD_MB=50`

Do not expose an unauthenticated Ollama server directly to the public internet. Put it behind private networking or authenticated access. Use persistent storage for `/data`; otherwise uploaded repositories and the SQLite index can disappear on redeploy. The GitHub clone feature requires Git in the image (included in the supplied Dockerfile).

For a quick local public demonstration, run the app and Ollama on the same machine and use a secure tunnel only if you understand the privacy implications. Do not upload private repositories to a public demo.

## Security and limitations

- Repository source is treated as untrusted input; the model is instructed not to follow instructions embedded in source files.
- The application does not run repository scripts, build commands, package installers, or tests.
- ZIP path traversal is rejected; upload size, file count, and file size are limited.
- Common secret filenames and secret-like lines are excluded from indexing. This is heuristic filtering, not a guarantee that all secrets are detected. Do not upload sensitive repositories to an untrusted deployment.
- The initial retrieval is keyword-based, not a vector/semantic RAG implementation. Embedding-based retrieval is a future enhancement.
- Dependency checks are not a vulnerability scanner. Verify versions with authoritative advisories.
- The app is a hackathon MVP, not a hardened multi-tenant production service. Add authentication, rate limits, per-user isolation, quotas, and stronger sandboxing before exposing it to the public.

## Development

```bash
python -m compileall backend
```

## Licence

MIT. See [LICENSE](LICENSE). Third-party model and dependency licences remain separate; review them before redistribution or commercial use.

### Render deployment note

A starter Render web service can build from the included `render.yaml`, but you must supply `OLLAMA_BASE_URL` pointing to a separately hosted, reachable Ollama-compatible endpoint. The persistent disk retains the SQLite database and indexed repository files. Keep the inference endpoint private/authenticated; this MVP does not include user authentication or rate limiting and should not be exposed as an unrestricted public multi-user service. For a public judging demo, use a controlled demo environment and avoid private repository uploads.

The included `sample-repositories/tiny-flask` directory is a safe, small example to ZIP and upload for the first demo.
