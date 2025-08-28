import os, random
from src.documents.loaders import load_pdf
from src.documents.cleaners import clean_text
from src.documents.splitters import split_documents
from src.documents.search import keyword_search
from src.utils.token import count_tokens

print("\n=== Démo complète des fonctions de traitement documents ===\n")
# --- 1. Sélection aléatoire d’un PDF ---
pdf_dir = "data/pdf"
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if not pdf_files:
    raise FileNotFoundError("Aucun PDF trouvé dans data/pdf !")

pdf_path = os.path.join(pdf_dir, random.choice(pdf_files))
print(f"📄 Fichier choisi : {pdf_path}")

# --- 2. Charger le PDF ---
docs = load_pdf(pdf_path)
print(f"✅ PDF chargé : {len(docs)} pages")

# --- 3. Nettoyer le contenu de chaque page ---
for d in docs:
    d.page_content = clean_text(d.page_content)
print("✅ Nettoyage effectué")

# --- 4. Split en chunks de 600 tokens ---
chunks = split_documents(docs, max_tokens=600, overlap_sentences=2)
print(f"✅ Split en {len(chunks)} chunks (~600 tokens chacun)")

# --- 5. Lancer une recherche simple ---
query = "John McCarthy"
results = keyword_search(chunks, query, k=3)

print(f"\n🔍 Résultats pour la requête: {query}\n")
for i, r in enumerate(results, 1):
    print(f"--- Résultat {i} ---\n{r}\n")

# --- 6. Vérifier la taille des premiers chunks ---
print("\n=== Aperçu des premiers chunks ===")
for i, c in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ({count_tokens(c.page_content)} tokens) ---")
    print(c.page_content)