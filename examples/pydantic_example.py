from pydantic import BaseModel, Field

# 1. Définir le modèle Pydantic
class ClassificationResult(BaseModel):
    category: str = Field(..., description="Catégorie assignée au texte (ex: IA, Cloud, etc.)")
    confidence: float = Field(..., description="Score de confiance entre 0 et 1")

from langchain_core.output_parsers import PydanticOutputParser

# 2. Définir le parser
classification_parser = PydanticOutputParser(pydantic_object=ClassificationResult)

from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import llm

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

# 4. Chaîne complète
classification_chain = classification_prompt | llm | classification_parser

# 5. Exécution
text = """
L'intelligence artificielle est une notion forgée au milieu des années 1950, dans la foulée des réflexions du mathématicien Alan Turing, qui se demandait si un ordinateur saurait un jour "penser", ou s’il n’était capable que d’un "jeu d’imitation" (imitation game). 
"""

response = classification_chain.invoke({
    "texte": text,
    "format_instructions": classification_chain.steps[-1].get_format_instructions()
})
print("Catégorie :", response.category)
print("Confiance :", response.confidence)