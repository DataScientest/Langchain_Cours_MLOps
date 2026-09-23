import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Live tests: RUN_LIVE=1 uv run pytest -m live (requires a valid GROQ_API_KEY).
RUN_LIVE = os.getenv("RUN_LIVE") == "1"

# No LangSmith tracing during tests (must run before the code calls load_dotenv).
os.environ["LANGSMITH_TRACING"] = "false"

if not RUN_LIVE:
    # Without a real key, every init_chat_model call (direct or through create_agent)
    # returns a fake model. Must happen before any src.* import.
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
    skip_live = pytest.mark.skip(reason="live test: run with RUN_LIVE=1 and a real API key")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
