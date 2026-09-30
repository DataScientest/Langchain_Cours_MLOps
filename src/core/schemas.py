from pydantic import BaseModel, Field

class ClassificationResult(BaseModel):
    category: str = Field(description="Catégorie choisie pour le texte")
    confidence: float = Field(
        ge=0,
        le=1,
        description="Score de confiance entre 0 et 1"
    )

class SummaryResult(BaseModel):
    summary: str = Field(description="Résumé court et fidèle du texte")

class TranslationResult(BaseModel):
    translated_text: str = Field(description="Texte traduit en anglais")
