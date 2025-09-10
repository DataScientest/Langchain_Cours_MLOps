from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# 1. Classification libre
class ClassificationResult(BaseModel):
    category: str = Field(..., description="Catégorie assignée au texte (ex: IA, Cloud, etc.)")
    confidence: float = Field(..., description="Score de confiance entre 0 et 1")

classification_parser = PydanticOutputParser(pydantic_object=ClassificationResult)

# 2. Résumé
class SummaryResult(BaseModel):
    summary: str = Field(..., description="Résume et veille à garder les mots clés les plus importants du texte d'origine.")

summary_parser = PydanticOutputParser(pydantic_object=SummaryResult)

# 3. Traduction
class TranslationResult(BaseModel):
    translated_text: str = Field(..., description="Texte traduit en anglais")

translation_parser = PydanticOutputParser(pydantic_object=TranslationResult)
