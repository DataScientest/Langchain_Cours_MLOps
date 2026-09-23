# Langchain_Cours_MLOps

## Version française

### Résumé Chapitre 5 : Intégration, agents modernes et observabilité

1. Agent documentaire (`src/agents/doc_agent.py`)
    - `create_agent` avec les tools `load_pdf_tool` et `clean_text_tool`.
    - `chat_agent` : agent de conversation avec `InMemorySaver`.

2. API FastAPI (`src/api/main.py`)
    - `/summary`, `/translate`, `/agent`, `/chat` (mémoire par `session_id`), `/history`.
    - Erreurs explicites avec `HTTPException`.

3. Observabilité avec LangSmith
    - Variables `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` dans `.env`.

Lancer l'API : `make api` puis ouvrir `http://127.0.0.1:8000/docs`.

## Lancer le projet et les tests

```bash
uv sync
uv run pytest       # tests hors ligne, sans clé API (modèles factices)
```

Les tests `live` appellent le vrai modèle et sont désactivés par défaut :

```bash
RUN_LIVE=1 uv run pytest -m live
```

Le modèle se configure dans `.env` avec `CHAT_MODEL` (par défaut `groq:openai/gpt-oss-120b`).

## English version

### Summary Chapter 5: Integration, modern agents and observability

1. Document agent (`src/agents/doc_agent.py`)
    - `create_agent` with the `load_pdf_tool` and `clean_text_tool` tools.
    - `chat_agent`: conversational agent with `InMemorySaver`.

2. FastAPI API (`src/api/main.py`)
    - `/summary`, `/translate`, `/agent`, `/chat` (memory per `session_id`), `/history`.
    - Explicit errors with `HTTPException`.

3. Observability with LangSmith
    - `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` variables in `.env`.

Start the API: `make api`, then open `http://127.0.0.1:8000/docs`.

## Run the project and the tests

```bash
uv sync
uv run pytest       # offline tests, no API key needed (fake models)
```

`live` tests call the real model and are disabled by default:

```bash
RUN_LIVE=1 uv run pytest -m live
```

The model is set in `.env` with `CHAT_MODEL` (default: `groq:openai/gpt-oss-120b`).
