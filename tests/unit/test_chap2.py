import runpy

from src.core.chains import classification_chain, summary_chain, translation_chain
from src.core.schemas import ClassificationResult, SummaryResult, TranslationResult
from src.prompts.prompts import classification_prompt


def test_classification_prompt_uses_few_shot_and_input():
    messages = classification_prompt.invoke({"input": "Docker en production"}).to_messages()
    assert [m.type for m in messages] == ["system", "human", "ai", "human", "ai", "human"]
    assert messages[-1].content == "Texte : Docker en production"


def test_chains_return_pydantic_objects():
    assert isinstance(classification_chain.invoke({"input": "texte"}), ClassificationResult)
    assert isinstance(summary_chain.invoke({"input": "texte"}), SummaryResult)
    assert isinstance(translation_chain.invoke({"input": "Bonjour"}), TranslationResult)


def test_chap2_script_runs(capsys):
    runpy.run_module("src.chap2_prompt_output", run_name="__main__")
    out = capsys.readouterr().out
    assert "Category:" in out and "Summary:" in out and "Translated text:" in out
