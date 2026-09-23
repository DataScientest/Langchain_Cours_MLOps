import runpy

from langchain_core.messages import AIMessage

from src.core.llm import llm
from src.core.tools import char_count, word_count


def test_tools():
    assert word_count.invoke("LangChain structure les applications") == 4
    assert char_count.invoke("abc") == 3


def test_llm_runnable_interface():
    assert isinstance(llm.invoke("Bonjour"), AIMessage)
    assert len(llm.batch(["a", "b"])) == 2
    assert "".join(chunk.content for chunk in llm.stream("Bonjour"))


def test_chap1_script_runs(capsys):
    runpy.run_module("src.chap1_fund_components", run_name="__main__")
    out = capsys.readouterr().out
    assert "--- INVOKE ---" in out and "--- BATCH ---" in out and "--- STREAMING ---" in out
