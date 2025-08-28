from src.core.chains import classification_chain, summary_chain, translation_chain

print("\n=== Démonstration Chapitre 2 : Classification, Résumé & Traduction ===\n")

# Texte de départ 
doc = """L'intelligence artificielle (IA) est l'ensemble des programmes ou algorithmes permettant aux machines d'effectuer des tâches typiquement associées à l'intelligence humaine, comme l'apprentissage, le raisonnement, la résolution de problème, la perception ou la prise de décision. L'intelligence artificielle est également le champ de recherche visant à développer de telles machines ainsi que les systèmes informatiques qui en résultent.

Souvent classée dans le domaine des mathématiques et des sciences cognitives, l'IA fait appel à des disciplines telles que la neurobiologie computationnelle (qui a notamment inspiré les réseaux neuronaux artificiels), les statistiques, ou l'algèbre linéaire. Elle vise à résoudre des problèmes à forte complexité logique ou algorithmique. Par extension, dans le langage courant, l'IA inclut les dispositifs imitant ou remplaçant l'homme dans certaines mises en œuvre de ses fonctions cognitives.

Les applications de l'IA couvrent de nombreux domaines, notamment les moteurs de recherche, les systèmes de recommandation, l'aide au diagnostic médical, la compréhension du langage naturel, les voitures autonomes, les chatbots, les outils de génération d'images, les outils de prise de décision automatisée, les programmes compétitifs dans des jeux de stratégie et certains personnages non-joueurs de jeu vidéo."""

# 1. Classification
print("--- Classification ---")
response = classification_chain.invoke({
    "texte": doc,
    "format_instructions": classification_chain.steps[-1].get_format_instructions()
})
print("Catégorie :", response.category)
print("Confiance :", response.confidence)

# 2. Résumé
print("\n--- Résumé ---")
response = summary_chain.invoke({
    "texte": doc,
    "format_instructions": summary_chain.steps[-1].get_format_instructions()
})
print("Résumé :", response.summary)

# 3. Traduction (avec streaming)
print("\n--- Traduction (Streaming) ---")
sentence = doc  
stream = translation_chain.stream({
    "texte": sentence,
    "format_instructions": translation_chain.steps[-1].get_format_instructions()
})

# Affichage progressif
result = None
for chunk in stream:
    result = chunk 

# Résultat final validé
print("Texte traduit :", result.translated_text)