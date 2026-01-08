import asyncio
import json

from openai import OpenAI

from system.app.core.config import settings
from system.app.domain.entities.email_entity import Email
from system.app.domain.entities.classification import (
    ClassificationResult,
    EmailCategory,
)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LLMClient:
    """
    Cliente de LLM usando OpenAI para classificar e gerar rascunho.
    """

    async def classify_email(self, email: Email) -> ClassificationResult:
        system_prompt = """
Você é um assistente especializado em atendimento ao cliente de e-commerce.

Sua tarefa é:
1) Classificar o e-mail do cliente em UMA das seguintes categorias EXATAS:
   - FEEDBACK_NEGATIVO: reclamações, insatisfação, problemas com produtos ou atendimento.
   - FEEDBACK_POSITIVO: elogios, satisfação, comentários positivos.
   - GARANTIA: produto defeituoso, quebrado, parou de funcionar, solicitação de garantia.
   - ARREPENDIMENTO_REEMBOLSO: cliente se arrependeu da compra, quer devolver ou reembolso.
   - DUVIDAS_GERAIS: perguntas sobre uso do produto, entrega, prazo, processo de compra, etc.
   - INCONCLUSIVO: não é possível determinar claramente.

2) Gerar um rascunho de resposta adequado, educado e profissional, em português,
   respondendo à situação do cliente.

3) Definir um nível de confiança (0 a 1) para a classificação.

4) Indicar se é necessário revisão humana (true/false):
   - true: caso o e-mail seja sensível, agressivo, muito confuso ou a confiança seja baixa (< 0.7).
   - false: caso seja um caso simples e a confiança seja alta (>= 0.7).

Responda SEMPRE em JSON puro, no formato:

{
  "classification": "FEEDBACK_NEGATIVO | FEEDBACK_POSITIVO | GARANTIA | ARREPENDIMENTO_REEMBOLSO | DUVIDAS_GERAIS | INCONCLUSIVO",
  "confidence": 0.0,
  "draft_reply": "texto do rascunho em português",
  "requires_human_review": true
}
"""

        user_content = f"""
E-mail do cliente:

Remetente: {email.from_email}
Assunto: {email.subject}
Corpo:
{email.body}
"""

        # A biblioteca da OpenAI é síncrona; usamos to_thread pra não travar o event loop.
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
        )

        content = completion.choices[0].message.content

        # Tenta parsear o JSON retornado
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # fallback defensivo caso o modelo quebre o formato
            return ClassificationResult(
                category=EmailCategory.INCONCLUSIVO,
                confidence=0.0,
                draft_reply=(
                    "Olá,\n\n"
                    "Obrigado pelo seu contato. Recebemos sua mensagem e ela será analisada "
                    "por nossa equipe de suporte em breve.\n\n"
                    "Atenciosamente,\nEquipe de Suporte"
                ),
                requires_human_review=True,
            )

        raw_class = data.get("classification", "INCONCLUSIVO")

        try:
            category = EmailCategory(raw_class)
        except ValueError:
            category = EmailCategory.INCONCLUSIVO

        confidence = float(data.get("confidence", 0.0))
        draft_reply = (data.get("draft_reply") or "").strip()
        requires_human_review = bool(data.get("requires_human_review", True))

        # Regra de negócio extra: abaixo do limiar, força revisão humana
        if confidence < 0.7:
            requires_human_review = True

        return ClassificationResult(
            category=category,
            confidence=confidence,
            draft_reply=(
                draft_reply
                or "Olá,\n\nObrigado pelo seu contato. Nossa equipe irá analisar seu caso.\n\nAtenciosamente,\nEquipe de Suporte"
            ),
            requires_human_review=requires_human_review,
        )