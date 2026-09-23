from src.core.chains import classification_chain, summary_chain, translation_chain

text = """
Artificial intelligence helps machines solve problems, analyze data,
and support humans in tasks such as diagnosis, recommendation, and automation.
"""

print("\n--- Classification ---")
classification = classification_chain.invoke({"input": text})
print("Category:", classification.category)
print("Confidence:", classification.confidence)

print("\n--- Summary ---")
summary = summary_chain.invoke({"input": text})
print("Summary:", summary.summary)

print("\n--- Translation ---")
translation = translation_chain.invoke({"input": "Bonjour, comment allez-vous ?"})
print("Translated text:", translation.translated_text)
