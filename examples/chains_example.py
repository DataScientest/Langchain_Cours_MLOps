from src.core.chains import classification_chain

print("\n=== Classification ===")

text = """
L'intelligence artificielle est une notion forgée au milieu des années 1950, dans la foulée des réflexions du mathématicien Alan Turing, qui se demandait si un ordinateur saurait un jour "penser", ou s’il n’était capable que d’un "jeu d’imitation" (imitation game). 
"""

response = classification_chain.invoke({
    "texte": text
})

print("AIMessage :", response.content)