# Langchain_Cours_MLOps

## Version française

### Résumé Chapitre 1 : Composants fondamentaux

1. Environnement de travail
    - Arborescence claire (`src/`, `data/`, etc.).
    - Dépendances gérées avec `uv` et `pyproject.toml` (LangChain 1.x, LangGraph 1.x).

2. Chat models
    - `init_chat_model` crée le modèle à partir de la variable `CHAT_MODEL` du fichier `.env`.
    - Changer de fournisseur revient à changer cette variable.

3. Messages
    - **SystemMessage** (rôle du modèle), **HumanMessage** (demande), **AIMessage** (réponse).

4. Tools
    - `word_count` et `char_count`, créés avec le décorateur `@tool` (`langchain.tools`).

5. Interface Runnable
    - `.invoke()`, `.batch()`, `.stream()`.

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

### Summary Chapter 1: Fundamental components

1. Working environment
    - Clear directory structure (`src/`, `data/`, etc.).
    - Dependencies managed with `uv` and `pyproject.toml` (LangChain 1.x, LangGraph 1.x).

2. Chat models
    - `init_chat_model` builds the model from the `CHAT_MODEL` variable in `.env`.
    - Switching provider means changing this variable.

3. Messages
    - **SystemMessage** (model role), **HumanMessage** (request), **AIMessage** (answer).

4. Tools
    - `word_count` and `char_count`, created with the `@tool` decorator (`langchain.tools`).

5. Runnable interface
    - `.invoke()`, `.batch()`, `.stream()`.

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
