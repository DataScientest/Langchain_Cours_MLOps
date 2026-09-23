from src.core.llm import llm
from src.core.schemas import (
    ClassificationResult,
    SummaryResult,
    TranslationResult,
)
from src.prompts.prompts import (
    classification_prompt,
    summary_prompt,
    translation_prompt,
)

classification_chain = classification_prompt | llm.with_structured_output(ClassificationResult, method="json_schema")
summary_chain = summary_prompt | llm.with_structured_output(SummaryResult, method="json_schema")
translation_chain = translation_prompt | llm.with_structured_output(TranslationResult, method="json_schema")
