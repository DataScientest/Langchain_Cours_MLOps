from langchain_core.prompts import ChatPromptTemplate

# Classification
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu classes un texte dans une seule catégorie métier."),
    ("human", "Texte : Le réseau de neurones analyse des radios."),
    ("ai", "Santé numérique"),
    ("human", "Texte : Kubernetes automatise le déploiement."),
    ("ai", "Cloud"),
    ("human", "Texte : {input}")
])

# Résumé
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu résumes un texte en conservant les idées essentielles."),
    ("human", "Texte : {input}")
])

# Traduction
translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu traduis du français vers l'anglais avec un style naturel."),
    ("human", "Texte : {input}")
])
