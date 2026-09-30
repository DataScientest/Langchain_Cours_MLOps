from langchain_core.messages import HumanMessage, SystemMessage
from src.core.llm import llm
from src.core.tools import word_count, char_count

print("\n=== Chapitre 1 : Composants fondamentaux ===\n")

print("--- INVOKE ---")
response = llm.invoke([
    SystemMessage(content="Tu es un assistant expert en MLOps."),
    HumanMessage(content="Explique en quoi LangChain aide à structurer une application LLM.")
])
print(response.content)

print("\n--- ANALYSE DE LA RÉPONSE ---")
print("Nombre de mots      :", word_count.invoke(response.content))
print("Nombre de caractères :", char_count.invoke(response.content))

print("\n--- BATCH ---")
batch_inputs = [
    [
        SystemMessage(content="Tu es un assistant de synonymes."),
        HumanMessage(content="Donne un synonyme de rapide.")
    ],
    [
        SystemMessage(content="Tu es un assistant scientifique."),
        HumanMessage(content="Explique ce qu'est un neurone artificiel.")
    ]
]

batch_outputs = llm.batch(batch_inputs)
for i, r in enumerate(batch_outputs, 1):
    print(f"\nRéponse {i} :", r.content)

print("\n--- STREAMING ---")
stream_text = ""
for chunk in llm.stream("Rédige un court paragraphe sur les usages des agents IA."):
    print(chunk.content, end="", flush=True)
    stream_text += chunk.content

print("\n\nAnalyse du texte généré en streaming :")
print("Nombre de mots      :", word_count.invoke(stream_text))
print("Nombre de caractères :", char_count.invoke(stream_text))
