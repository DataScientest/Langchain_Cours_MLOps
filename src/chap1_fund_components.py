# examples/chap1_fond_comp.py

from langchain_core.messages import HumanMessage, SystemMessage
from src.core.runnable import run_invoke, run_batch, run_stream, run_with_retry
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

# 2. Utiliser notre Runnable invoke
print("\n--- Runnable .invoke ---")
response_text = run_invoke(human_prompt)
print("AIMessage     :", response_text)

# 3. Passer la réponse de l'IA dans nos outils
print("\n--- Analyse avec Tools ---")
print("Texte généré par l'IA :", response_text)
print("Nb de mots            :", word_count.invoke(response_text))
print("Nb de caractères      :", char_count.invoke(response_text))

# 4. Montrer .batch avec plusieurs prompts
print("\n--- Runnable .batch ---")
batch_outputs = run_batch([
    "Donne-moi un synonyme de 'rapide'.",
    "Donne-moi un synonyme de 'heureux'."
])
print("Batch outputs :", batch_outputs)

# 5. Streaming (génération progressive)
print("\n--- Runnable .stream ---")
run_stream("Écris un poème sur les modèles de langage.")

# 6. Retry automatique en cas d'échec
print("\n--- Runnable .with_retry ---")
retry_output = run_with_retry("Dis 'Bonjour' après un retry.")
print("Retry output  :", retry_output)
