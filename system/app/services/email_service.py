# system/app/services/email_service.py
from system.app.domain.entities.email_entity import Email
from system.app.domain.entities.classification import EmailCategory
from system.app.infrastructure.llm.openai_client import DummyLLMClient
from system.app.infrastructure.llm.llm_client import OpenAILLMClient
from system.app.schemas.email_schemas import EmailCreateRequest


class EmailClassificationService:
    def __init__(self, llm_client: OpenAILLMClient | None = None):
        self._llm_client = llm_client or OpenAILLMClient()

    async def classify_from_request(self, payload: EmailCreateRequest) -> Email:
        email = Email(
            id=None,
            from_email=payload.from_email,
            subject=payload.subject,
            body=payload.body,
            category=EmailCategory.INCONCLUSIVO,
            confidence=0.0,
            draft_reply="",
            requires_human_review=True,
        )

        result = await self._llm_client.classify_email(email)

        email.category = result.category
        email.confidence = result.confidence
        email.draft_reply = result.draft_reply
        email.requires_human_review = result.requires_human_review

        return email