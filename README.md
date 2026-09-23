# Langchain_Cours_MLOps

## Version française

### Résumé Chapitre 3 : Traitement de documents

1. Loaders (`src/documents/loaders.py`)
    - PDF (`PyPDFLoader`), texte (`TextLoader`), web (`WebBaseLoader`) → objets `Document`.

2. Nettoyage (`src/documents/cleaners.py`)
    - Suppression des numéros de page isolés et des espaces multiples.

3. Découpage (`src/documents/splitters.py`)
    - `RecursiveCharacterTextSplitter` (`chunk_size=800`, `chunk_overlap=150`).

4. Tokens (`src/utils/token.py`)
    - Estimation avec `tiktoken` (`cl100k_base`).

5. Recherche par mot-clé et tools (`src/documents/search.py`, `src/documents/tools.py`).

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

### Summary Chapter 3: Document processing

1. Loaders (`src/documents/loaders.py`)
    - PDF (`PyPDFLoader`), text (`TextLoader`), web (`WebBaseLoader`) → `Document` objects.

2. Cleaning (`src/documents/cleaners.py`)
    - Removes isolated page numbers and repeated whitespace.

3. Splitting (`src/documents/splitters.py`)
    - `RecursiveCharacterTextSplitter` (`chunk_size=800`, `chunk_overlap=150`).

4. Tokens (`src/utils/token.py`)
    - Estimate with `tiktoken` (`cl100k_base`).

5. Keyword search and tools (`src/documents/search.py`, `src/documents/tools.py`).

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
