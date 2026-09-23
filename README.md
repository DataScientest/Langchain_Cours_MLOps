# Langchain_Cours_MLOps

## Version française

### Résumé Chapitre 2 : Prompts et sorties structurées

1. `ChatPromptTemplate`
    - Prompts réutilisables avec des variables (`{input}`), rangés dans `src/prompts/prompts.py`.

2. Few-shot learning
    - Exemples `human` / `ai` dans le prompt de classification.

3. Schémas Pydantic (`src/core/schemas.py`)
    - `ClassificationResult`, `SummaryResult`, `TranslationResult`.

4. Chaînes (`src/core/chains.py`)
    - `prompt | llm.with_structured_output(Schema)` : la sortie est directement un objet Pydantic valide.

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

### Summary Chapter 2: Prompts and structured output

1. `ChatPromptTemplate`
    - Reusable prompts with variables (`{input}`), stored in `src/prompts/prompts.py`.

2. Few-shot learning
    - `human` / `ai` examples in the classification prompt.

3. Pydantic schemas (`src/core/schemas.py`)
    - `ClassificationResult`, `SummaryResult`, `TranslationResult`.

4. Chains (`src/core/chains.py`)
    - `prompt | llm.with_structured_output(Schema)`: the output is directly a valid Pydantic object.

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
