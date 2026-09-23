import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Tests live : RUN_LIVE=1 uv run pytest -m live (nécessite GROQ_API_KEY valide).
RUN_LIVE = os.getenv("RUN_LIVE") == "1"

# Pas de traçage LangSmith pendant les tests (doit précéder le load_dotenv du code).
os.environ["LANGSMITH_TRACING"] = "false"

if not RUN_LIVE:
    # Sans clé réelle : tout appel à init_chat_model (direct ou via create_agent)
    # renvoie un modèle factice. Doit être fait avant d'importer src.*.
    import langchain.agents.factory
    import langchain.chat_models

    from tests.fakes import fake_init_chat_model

    os.environ["GROQ_API_KEY"] = "test-key"
    langchain.chat_models.init_chat_model = fake_init_chat_model
    langchain.agents.factory.init_chat_model = fake_init_chat_model


@pytest.fixture(autouse=True)
def _run_from_repo_root(monkeypatch):
    monkeypatch.chdir(ROOT)


def pytest_collection_modifyitems(config, items):
    if RUN_LIVE:
        return
    skip_live = pytest.mark.skip(reason="test live : lancer avec RUN_LIVE=1 et une vraie clé API")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
