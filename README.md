# Langchain_Cours_MLOps

## Version française

### Résumé Chapitre 4 : État et mémoire

1. `checkpointer` et `thread_id`
    - `create_agent(..., checkpointer=InMemorySaver())` conserve l'état de chaque conversation.
    - Le `thread_id` passé dans `config` identifie la conversation.

2. Plusieurs utilisateurs
    - Un `thread_id` par utilisateur : les historiques d'Alice, Bob et Charlie restent séparés (`src/chap4_memory.py`).

3. Optimiser l'historique
    - Fenêtrage, résumé, mémoire ciblée : renvoyer le bon contexte au bon moment.

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

### Summary Chapter 4: State and memory

1. `checkpointer` and `thread_id`
    - `create_agent(..., checkpointer=InMemorySaver())` keeps the state of each conversation.
    - The `thread_id` passed in `config` identifies the conversation.

2. Several users
    - One `thread_id` per user: Alice, Bob and Charlie keep separate histories (`src/chap4_memory.py`).

3. Optimising the history
    - Windowing, summaries, targeted memory: send the right context at the right time.

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
