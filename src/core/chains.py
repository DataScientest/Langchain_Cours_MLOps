from .llm import llm
from src.prompts.prompts import (
    summary_prompt,
    classification_prompt,
    translation_prompt,
)
from src.core.parsers import (
    classification_parser,
    summary_parser,
    translation_parser,
)

# 1. Résumé automatique
summary_chain = summary_prompt | llm | summary_parser

# 2. Classification libre
classification_chain = classification_prompt | llm | classification_parser

# 3. Traduction
translation_chain = translation_prompt | llm | translation_parser
