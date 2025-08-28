from langchain_core.prompts import ChatPromptTemplate

# Classification 
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant qui propose une catégorie pertinente pour un texte."),
    
    # Few-shot
    ("human", 
     "Texte : 'Les réseaux de neurones profonds révolutionnent l'apprentissage automatique.'"),
    ("ai", '{{"category": "Intelligence Artificielle", "confidence": 0.95}}'),
    
    ("human", 
     "Texte : 'Docker et Kubernetes facilitent le déploiement d’applications dans le cloud.'"),
    ("ai", '{{"category": "Cloud", "confidence": 0.9}}'),
    
    # Instruction générale
    ("human",
     "Analyse le texte suivant et propose UNIQUEMENT une seule catégorie adaptée :\n\n"
     "Texte : {texte}\n\n"
     "{format_instructions}")
])

# Résumé 
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant qui résume des textes."),
    
    # Few-shot
    ("human", 
     "Résume le texte suivant de la façon la plus concise possible :\n\n"
     "Texte : L'intelligence artificielle est un domaine en pleine expansion, "
     "qui combine mathématiques, informatique et sciences cognitives."),
    ("ai", 
     '{{"summary": "L’IA est un domaine en croissance qui associe mathématiques, informatique et sciences cognitives."}}'),
    
    # Instruction générale
    ("human", 
     "Résume le texte suivant de la façon la plus concise possible.\n\n"
     "IMPORTANT : Réponds UNIQUEMENT avec un JSON valide, sans texte en dehors du JSON.\n\n"
     "Texte : {texte}\n\n"
     "{format_instructions}")
])

# Traduction
translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un traducteur professionnel."),
    
    # Few-shot
    ("human", "Texte : 'Bonjour, comment vas-tu ?'"),
    ("ai", '{{"translated_text": "Hello, how are you?"}}'),
    
    # Instruction générale
    ("human", 
     "Traduis ce texte en anglais : {texte}\n\n"
     "{format_instructions}")
])