# Repo Séance architecture

```mermaid
flowchart TD
  A[Browser UI] --> B[FastAPI]
  B --> C[GitHub / ZIP ingestion]
  C --> D[Safe static file scanner]
  D --> E[Code chunks + file/line metadata]
  E --> F[(SQLite index)]
  B --> G[Evidence retrieval]
  F --> G
  G --> H[Ollama local open-weight model]
  H --> I[Grounded answer + source references]
  B --> J[Autopsy and Markdown report]
```

## Trust boundaries

Imported repositories are untrusted. The MVP reads text files only and does not execute project code. The model receives retrieved text as evidence and is explicitly instructed not to follow instructions contained in that text. Secret filtering is best-effort and is not a substitute for reviewing the data before upload.
