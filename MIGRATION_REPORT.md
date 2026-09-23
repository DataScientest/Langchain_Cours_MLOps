# Rapport de migration LangChain 1.x : Langchain_Cours_MLOps

Date : 2026-09-23. Cours source de vérité : `Learn_Content/Science/MLOps/{FR,EN}/Courses/langchain_llmops_*`.

## Pourquoi

Les branches `chap1` à `chap5` épinglaient `langchain==0.3.27` sans `langgraph`, alors que le cours enseigne LangChain 1.x (`init_chat_model`, `with_structured_output`, `create_agent`, `InMemorySaver`).
Elles contenaient aussi un autre projet que celui du cours (LiteLLM, `PydanticOutputParser`, `SessionManager`, API avec cookies, Streamlit).
L'élève suivait donc un cours 1.x avec un environnement 0.3 et un code différent.

De plus, le modèle de référence `groq:llama-3.3-70b-versatile` a été arrêté par Groq le 2026-08-16 (tiers free et developer, voir https://console.groq.com/docs/deprecations).

## Versions avant / après

Vérifiées sur PyPI le 2026-09-23. Identiques dans les 5 branches, dans le cours et dans `exam_Langchain` (`scripts/check_versions.sh`).

| Paquet | Avant (branches) | Avant (cours) | Après |
|---|---|---|---|
| langchain | 0.3.27 | 1.2.12 | 1.4.2 |
| langchain-core | 0.3.74 | 1.2.20 | 1.6.4 |
| langchain-community | 0.3.27 | 0.4.1 | 0.4.2 |
| langgraph | absent | 1.1.3 | 1.2.12 |
| langsmith | absent | 0.7.20 | 0.14.0 |
| langchain-groq | absent | 1.1.2 | 1.1.3 |
| langchain-openai | absent | 1.1.11 | 1.6.4 |
| langchain-litellm | 0.2.2 | absent | supprimé (pas utilisé par le cours) |
| langchain-text-splitters | absent | 1.0.0 | 1.1.2 |
| pydantic | 2.11.7 | 2.11.7 | 2.13.5 |
| python-dotenv | 1.1.1 | 1.1.1 | 1.2.3 |
| pypdf | 6.0.0 | 6.0.0 | 6.19.0 |
| tiktoken | 0.11.0 | 0.11.0 | 0.14.0 |
| beautifulsoup4 | absent | absent | 4.15.0 (requis par `WebBaseLoader`) |
| fastapi | 0.116.1 | 0.116.1 | 0.141.1 |
| uvicorn | 0.35.0 | 0.35.0 | 0.53.0 |
| python-multipart | 0.0.20 | 0.0.20 | 0.0.32 |
| streamlit / agents | 1.50.0 / 1.4.0 | absent | supprimés (pas utilisés par le cours) |
| pytest / httpx (dev) | absent | absent | 9.1.1 / 0.28.1 |

Les dépendances arrivent au même chapitre que dans le cours : socle au chap1, `uv add` documentaire au chap3, `uv add` FastAPI au chap5.
Les dépendances du `pyproject.toml` de chaque branche sont celles qu'obtient un élève qui suit le cours.
Les branches ajoutent seulement un groupe `[dependency-groups] dev` (pytest, httpx) et la section `[tool.pytest.ini_options]`, absents du cours.

Modèle : `CHAT_MODEL=groq:openai/gpt-oss-120b` (remplaçant recommandé par Groq ; tools et JSON Schema supportés). Il se change dans `.env` sans toucher au code.
Limites constatées sur un compte Groq gratuit : 8 000 tokens par minute et 200 000 tokens par jour, **par organisation** (deux clés d'un même compte partagent le quota).

## Branches et fichiers

| Branche cible | Branche de travail |
|---|---|
| `main` | `feature/no-ref/align-skeleton-langchain-v1` |
| `chap1` … `chap5` | `feature/no-ref/migrate-langchain-v1-chapN` |

- `main` (squelette vide cloné par l'élève) : `parsers.py` remplacé par `schemas.py`, `memory/memory.py` et `app.py` supprimés, README réécrit (FR + EN).
- `chapN` : code du cours des chapitres 1 à N, recopié à l'identique, avec les correctifs listés plus bas.
- Supprimés après vérification qu'aucun autre fichier, ni le cours, ni l'examen ne les utilisent : `src/core/parsers.py`, `src/memory/memory.py`, `src/app.py`, le splitter maison, `SessionManager`, l'authentification par cookie, `/upload_file`, `/doc_classify`, les tools `load_txt_tool`, `load_markdown_tool`, `split_texts_tool` et `set_corpus_tool`.
- Supprimés : les fichiers `.pyc` commités par erreur ; `.gitignore` complété.
- `.env` : placeholders uniquement, variables `CHAT_MODEL`, `USER_AGENT` (chap3+) et `LANGSMITH_*` (chap5).
- Ajoutés : `tests/`, `scripts/check_versions.sh`, cible `make test`.

## APIs migrées

| Avant | Après |
|---|---|
| `ChatLiteLLM` + fallback manuel | `init_chat_model(os.getenv("CHAT_MODEL", ...))` |
| `from langchain.agents import tool` (supprimé en 1.x) | `from langchain.tools import tool` |
| `PydanticOutputParser` + `format_instructions` | `prompt \| llm.with_structured_output(Schema)` |
| `RunnableWithMessageHistory` + `FileChatMessageHistory` / `SQLChatMessageHistory` | `create_agent(..., checkpointer=InMemorySaver())` + `thread_id` |
| `initialize_agent(..., AgentType.ZERO_SHOT_REACT_DESCRIPTION)` | `langchain.agents.create_agent` |
| Splitter maison par phrases | `langchain_text_splitters.RecursiveCharacterTextSplitter` |
| `LANGCHAIN_TRACING_V2` / `LANGCHAIN_API_KEY` | `LANGSMITH_TRACING` / `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT` |

`from langchain.chat_models import init_chat_model` est l'import canonique de la v1 (ce n'est pas l'ancien `langchain.chat_models.ChatOpenAI`).

Pas d'embeddings dans ce module : le RAG du chap3 est présenté comme concept, sans code. Le point `text-embedding-ada-002` ne s'applique donc pas.

## Correctifs issus des tests avec le vrai modèle

Les modèles factices ne pouvaient pas les révéler. Ils ont été trouvés en exécutant le cours contre `groq:openai/gpt-oss-120b`, puis confirmés par l'apprenant simulé.

| Problème | Correctif (cours FR/EN + branches) |
|---|---|
| Chap2 : `with_structured_output` par défaut (function calling) échoue 4 fois sur 5 (`tool_use_failed`) avec le prompt few-shot | `method="json_schema"` : 15/15 |
| Chap5 : l'agent envoie tout le PDF au modèle (≈ 8 700 tokens), HTTP 413 en compte gratuit | `truncate_to_tokens` (`src/utils/token.py`) + `read_pdf_excerpt_tool` (`src/documents/tools.py`), extrait nettoyé borné à 1 500 tokens ; l'agent n'a plus que ce tool |
| Chap5 : `response_format=DocAnswer` → HTTP 400 (Groq refuse le mode JSON natif combiné à des tools) | `ToolStrategy(DocAnswer)` |
| Chap3 : `USER_AGENT` du `.env` jamais chargé (lu à l'import de `WebBaseLoader`) | `load_dotenv()` avant l'import dans `loaders.py` |
| Chap5 : `LANGSMITH_TRACING=true` avec une clé placeholder → 403 à chaque trace | `.env` modèle en `false` + phrase dans le cours |
| Chap5 : erreurs du fournisseur remontées en 500 ; fichier absent en 502 | `/agent` : 400 chemin vide, 404 fichier absent, 413/429 transmis, 502 sinon |
| Chap1/5 : limites du compte gratuit et message utilisateur conservé après un `/chat` en échec, non documentés | Notes ajoutées au cours ; commande `uvicorn` de repli `--port 8001` |

Les docstrings du nouveau code et du code de test sont en anglais. Le code recopié du cours FR garde ses docstrings françaises d'origine (voir points non résolus).

## Bugs corrigés au passage

- chap2 (ancien code) : le script envoyait `"texte"` à des prompts qui attendent `{input}`.
- Cours chap3 : `keyword_search(chunks, "LangChain")` ne trouvait rien, car `data/pdf/1.pdf` est l'article Wikipédia « Intelligence artificielle ». L'exemple cherche maintenant `"McCarthy"`.
- Cours chap5 : `/history` utilisait `checkpointer` (non importé dans `main.py`) et renvoyait des objets non sérialisables. Il utilise maintenant `chat_agent.get_state(...)`.

## Tests

`uv sync && uv run pytest` dans chaque branche, sans clé API. Les modèles factices sont `GenericFakeChatModel` (tool_calls simulés) et un modèle scripté qui remplace `init_chat_model`.

| Branche | Résultat |
|---|---|
| chap1 | 17 passed, 7 deselected (live) |
| chap2 | 20 passed, 7 deselected |
| chap3 | 26 passed, 7 deselected |
| chap4 | 28 passed, 7 deselected |
| chap5 | 38 passed, 7 deselected |

Couverture :
- imports ;
- `prompt | modèle factice.with_structured_output(Pydantic)` ;
- tool appelé par un agent `create_agent` avec `GenericFakeChatModel` ;
- mémoire sur 2 tours avec le même `thread_id`, et un autre thread vide ;
- exécution de chaque script `chapN_*.py` tel qu'il est écrit dans le cours ;
- pipeline documentaire sur les vrais PDF ;
- endpoints FastAPI via `TestClient` (chap5, où FastAPI entre dans le cours) ;
- `response_format` / `structured_response`.

Aucun `DeprecationWarning` hors celui de `langchain-community` (voir plus bas), vérifié avec `-W error::DeprecationWarning`.

Tests live (`RUN_LIVE=1 uv run pytest -m live`, 7 tests : modèle, 3 × chaînes structurées, agent documentaire sur `1.pdf`, `ToolStrategy`, mémoire) :
- `groq:openai/gpt-oss-120b` : 7/7 sur le code avant les derniers ajouts (extrait à 1 500 tokens, gestion d'erreurs) ; relance sur le code final **en attente** du quota journalier Groq ;
- `openai:gpt-5.4-mini` via la gateway Liora : 7/7 sur le code final.

## Test de bout en bout (apprenant simulé)

Un agent Codex a joué un apprenant : dépôt neuf, cours FR lu dans l'ordre, chaque fichier recopié, chaque commande exécutée, exercices tentés puis comparés à la solution, API testée avec `curl`.

| Passage | Cours | Modèle | OK | KO | Ambigu |
|---|---|---|---:|---:|---:|
| 1 | avant correctifs | `groq:openai/gpt-oss-120b` | 16 | 5 | 1 |
| 2 | après correctifs | `openai:gpt-5.4-mini` (gateway Liora, quota Groq épuisé) | 26 | 0 | 2 |

Les 2 points ambigus du 2e passage (fichier absent en 502, port 8000 occupé) sont corrigés depuis.
Un passage complet avec relances a consommé presque tout le quota journalier d'un compte Groq gratuit.

`scripts/check_versions.sh` : OK sur les 5 branches de travail + `exam_Langchain/pyproject.toml` (27 paquets). Il échoue, comme attendu, sur les anciennes branches `origin/chapN`.
Après merge : `scripts/check_versions.sh` ; avant merge : `REFS="feature/no-ref/migrate-langchain-v1-chap1 …" scripts/check_versions.sh`.

grep final (hors `uv.lock`) : aucune occurrence de `langchain==0.3`, `LLMChain`, `initialize_agent`, `AgentExecutor`, `ConversationChain`, `create_react_agent`, `RunnableWithMessageHistory`, `PydanticOutputParser`, `litellm` ou `llama-3`.

## Extraits de code du cours

Les 96 blocs Python du cours (48 FR + 48 EN) ont été exécutés avec les versions ci-dessus et un modèle factice :

- 72 blocs s'exécutent seuls ;
- 24 blocs sont des suites de blocs précédents (`#previous imports`, `response = ...` après une chaîne, exemples à compléter). Ils s'exécutent une fois enchaînés au bloc qui les précède dans le texte.

Deux cas ne sont pas vérifiables par ce harnais et sont couverts par les tests de chap5 :

- `response_format=DocAnswer` : `test_agent_structured_response_format` ;
- la variante de `/agent` avec `HTTPException`, qui remplace la première : `test_agent_endpoint_rejects_empty_path`.

## Points non résolus

- Relance des tests live sur Groq avec le code final : en attente du quota journalier.
- Le code recopié du cours FR a des docstrings en français (convention : code en anglais). À traiter dans le cours si souhaité.
- Écarts entre l'énoncé d'examen et les chapitres 1 à 5 (relevés par l'apprenant, antérieurs à cette migration) : authentification entre deux services, Docker/Compose/Makefile, historique des endpoints non-chat, pipeline conditionnel `/full_pipeline`, « chaîne de chat libre » au lieu d'un agent avec checkpointer.

- `langchain-community` est archivé depuis juin 2026 et émet un `DeprecationWarning` à l'import. Aucun package officiel ne reprend `PyPDFLoader`, `TextLoader` ni `WebBaseLoader`. Le seul partenaire PDF léger, `langchain-pymupdf4llm`, a été testé et écarté : sortie bruitée, lenteur, licence AGPL, Tesseract requis. Il reste épinglé en 0.4.2 (choix validé) ; à réévaluer si LangChain publie un remplaçant.
- Tests live non exécutés, faute de clé Groq valide.
- Le cours ne mentionne pas les branches `chapN` : l'élève clone `main` (squelette). Ajouter une phrase dans le cours pour signaler les corrections par branche serait utile, mais c'est un choix éditorial.
