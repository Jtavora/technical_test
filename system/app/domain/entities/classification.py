from enum import Enum
from dataclasses import dataclass


class EmailCategory(str, Enum):
    FEEDBACK_NEGATIVO = "FEEDBACK_NEGATIVO"
    FEEDBACK_POSITIVO = "FEEDBACK_POSITIVO"
    GARANTIA = "GARANTIA"
    ARREPENDIMENTO_REEMBOLSO = "ARREPENDIMENTO_REEMBOLSO"
    DUVIDAS_GERAIS = "DUVIDAS_GERAIS"
    INCONCLUSIVO = "INCONCLUSIVO"


@dataclass
class ClassificationResult:
    category: EmailCategory
    confidence: float
    draft_reply: str
    requires_human_review: bool