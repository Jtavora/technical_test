# system/app/infrastructure/llm/openai_client.py
from system.app.domain.entities.email_entity import Email
from system.app.domain.entities.classification import (
    ClassificationResult,
    EmailCategory,
)


class DummyLLMClient:
    async def classify_email(self, email: Email) -> ClassificationResult:
        body_lower = email.body.lower()

        if "reclamação" in body_lower or "problema" in body_lower:
            category = EmailCategory.FEEDBACK_NEGATIVO
        elif "elogio" in body_lower or "gostei" in body_lower:
            category = EmailCategory.FEEDBACK_POSITIVO
        elif "garantia" in body_lower or "defeito" in body_lower:
            category = EmailCategory.GARANTIA
        elif "arrependi" in body_lower or "reembolso" in body_lower:
            category = EmailCategory.ARREPENDIMENTO_REEMBOLSO
        elif "dúvida" in body_lower or "pergunta" in body_lower:
            category = EmailCategory.DUVIDAS_GERAIS
        else:
            category = EmailCategory.INCONCLUSIVO

        draft = f"""Olá,

Obrigado pelo contato. Sua mensagem foi classificada como: {category.value}.
Nossa equipe irá analisar e responder em breve.

Atenciosamente,
Equipe de Suporte
"""

        return ClassificationResult(
            category=category,
            confidence=0.7,
            draft_reply=draft,
            requires_human_review=True,
        )