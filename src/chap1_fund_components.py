from langchain_core.messages import HumanMessage, SystemMessage
from src.core.llm import llm
from src.core.tools import word_count, char_count

print("\n=== Chapitre 1 : Composants Fondamentaux ===\n")

# 1. Préparer les messages (System + Human)
human_prompt = "Explique en une phrase ce qu'est LangChain."

messages = [
    SystemMessage(content="Tu es un Assistant Intelligent de Documents."),
    HumanMessage(content=human_prompt)
]

print("--- Messages ---")
print("SystemMessage :", messages[0].content)
print("HumanMessage  :", messages[1].content)

# 2. Utiliser directement le Runnable (llm) avec .invoke
print("\n--- Runnable .invoke ---")
response = llm.invoke(messages)
response_text = response.content
print("AIMessage     :", response_text)

# 3. Passer la réponse de l'IA dans nos outils
print("\n--- Analyse avec Tools ---")
print("Texte généré par l'IA :", response_text)
print("Nb de mots            :", word_count.invoke(response_text))
print("Nb de caractères      :", char_count.invoke(response_text))

# 4. Montrer .batch avec plusieurs prompts
print("\n--- Runnable .batch ---")
batch_inputs = [
    [HumanMessage(content="Donne-moi un synonyme de 'rapide'.")],
    [HumanMessage(content="Donne-moi un synonyme de 'heureux'.")]
]
batch_outputs = llm.batch(batch_inputs)
print("Batch outputs :", [r.content for r in batch_outputs])

# 5. Streaming (génération progressive)
print("\n--- Runnable .stream ---")
for chunk in llm.stream([HumanMessage(content="Écris un poème sur les modèles de langage.")]):
    print(chunk.content, end="", flush=True)
print("\n--- End of stream ---")

# 6. Retry automatique en cas d'échec
print("\n--- Runnable .with_retry ---")
safe_llm = llm.with_retry()
retry_response = safe_llm.invoke([HumanMessage(content="Dis 'Bonjour' après un retry.")])
print("Retry output  :", retry_response.content)
