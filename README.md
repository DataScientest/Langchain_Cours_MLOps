# Langchain_Cours_MLOps
## Version française

Ce dépôt contient la structure de projet du cours LangChain & MLOps (LangChain 1.x, LangGraph 1.x).
Les fichiers sont volontairement vides : vous les complétez au fil des chapitres.

```txt
.
├── .env                          # Clés API et CHAT_MODEL (chapitre 1)
├── Makefile
├── README.md
├── pyproject.toml                # Dépendances (chapitre 1)
├── data
│   └── pdf
│       ├── 1.pdf
│       ├── 2.pdf
│       └── 3.pdf
└── src
    ├── chap1_fund_components.py  # Chapitre 1 : composants fondamentaux
    ├── chap2_prompt_output.py    # Chapitre 2 : prompts & sorties structurées
    ├── chap3_docs.py             # Chapitre 3 : traitement de documents
    ├── chap4_memory.py           # Chapitre 4 : état et mémoire
    ├── agents
    │   └── doc_agent.py          # Agents create_agent (chapitre 5)
    ├── api
    │   └── main.py               # API FastAPI (chapitre 5)
    ├── core
    │   ├── chains.py             # Chaînes prompt | llm.with_structured_output(...)
    │   ├── llm.py                # Modèle (init_chat_model)
    │   ├── schemas.py            # Schémas Pydantic
    │   └── tools.py              # Tools @tool
    ├── documents
    │   ├── cleaners.py           # Nettoyage des documents
    │   ├── loaders.py            # Chargement des documents
    │   ├── search.py             # Recherche par mot-clé
    │   ├── splitters.py          # Découpage en chunks
    │   └── tools.py              # Tools documentaires
    ├── memory
    │   └── session.py            # checkpointer + thread_id
    ├── prompts
    │   └── prompts.py            # ChatPromptTemplate
    └── utils
        └── token.py              # Comptage des tokens
```

👉 Chaque branche `chap1` à `chap5` contient la correction du chapitre correspondant, avec une suite de tests (`uv run pytest`) qui tourne sans clé API.

## English version

This repository contains the project structure of the LangChain & MLOps course (LangChain 1.x, LangGraph 1.x).
The files are intentionally empty: you fill them in chapter after chapter.

```txt
.
├── .env                          # API keys and CHAT_MODEL (chapter 1)
├── Makefile
├── README.md
├── pyproject.toml                # Dependencies (chapter 1)
├── data
│   └── pdf
│       ├── 1.pdf
│       ├── 2.pdf
│       └── 3.pdf
└── src
    ├── chap1_fund_components.py  # Chapter 1: fundamental components
    ├── chap2_prompt_output.py    # Chapter 2: prompts & structured output
    ├── chap3_docs.py             # Chapter 3: document processing
    ├── chap4_memory.py           # Chapter 4: state and memory
    ├── agents
    │   └── doc_agent.py          # create_agent agents (chapter 5)
    ├── api
    │   └── main.py               # FastAPI API (chapter 5)
    ├── core
    │   ├── chains.py             # prompt | llm.with_structured_output(...) chains
    │   ├── llm.py                # Model (init_chat_model)
    │   ├── schemas.py            # Pydantic schemas
    │   └── tools.py              # @tool tools
    ├── documents
    │   ├── cleaners.py           # Document cleaning
    │   ├── loaders.py            # Document loading
    │   ├── search.py             # Keyword search
    │   ├── splitters.py          # Chunk splitting
    │   └── tools.py              # Document tools
    ├── memory
    │   └── session.py            # checkpointer + thread_id
    ├── prompts
    │   └── prompts.py            # ChatPromptTemplate
    └── utils
        └── token.py              # Token counting
```

👉 Branches `chap1` to `chap5` hold the solution of each chapter, with a test suite (`uv run pytest`) that runs without any API key.
