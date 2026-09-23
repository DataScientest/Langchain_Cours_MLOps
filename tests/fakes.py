"""Modèles factices pour tester le cours sans clé API."""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool


class ToolCallingFakeChatModel(GenericFakeChatModel):
    """GenericFakeChatModel qui accepte bind_tools (requis par create_agent).

    Les réponses (y compris les tool_calls simulés) sont fournies à l'avance
    via `messages=iter([...])`.
    """

    def bind_tools(self, tools, **kwargs):
        return self


def _dummy_value(spec: dict[str, Any]) -> Any:
    kind = spec.get("type")
    if kind == "string":
        return "valeur factice"
    if kind in ("number", "integer"):
        low, high = spec.get("minimum", 0), spec.get("maximum", 1)
        value = (low + high) / 2
        return int(value) if kind == "integer" else value
    if kind == "boolean":
        return True
    if kind == "array":
        return []
    if kind == "object":
        return {}
    return None


class ScriptedFakeChatModel(BaseChatModel):
    """Modèle factice déterministe utilisé à la place de `init_chat_model`.

    - Sortie structurée (`with_structured_output`) : renvoie un tool_call dont
      les arguments respectent le schéma Pydantic demandé.
    - Sinon : répond en recopiant les messages humains reçus, ce qui permet de
      vérifier le contenu de la mémoire d'une conversation.
    """

    bound_tools: list[Any] = []
    tool_choice: Any = None

    @property
    def _llm_type(self) -> str:
        return "scripted-fake"

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        return self.model_copy(update={"bound_tools": list(tools), "tool_choice": tool_choice})

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        if self.tool_choice and self.bound_tools:
            function = convert_to_openai_tool(self.bound_tools[0])["function"]
            properties = function.get("parameters", {}).get("properties", {})
            args = {name: _dummy_value(spec) for name, spec in properties.items()}
            message = AIMessage(
                content="",
                tool_calls=[{"name": function["name"], "args": args, "id": "call_fake"}],
            )
        else:
            humans = [m.content for m in messages if isinstance(m, HumanMessage)]
            message = AIMessage(content="Réponse factice. Contexte : " + " | ".join(map(str, humans)))
        return ChatResult(generations=[ChatGeneration(message=message)])


def fake_init_chat_model(*args, **kwargs) -> ScriptedFakeChatModel:
    return ScriptedFakeChatModel()
