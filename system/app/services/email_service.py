from system.app.domain.entities.email_entity import Email
from system.app.domain.entities.classification import EmailCategory
from system.app.infrastructure.llm.llm_client import LLMClient
from system.app.infrastructure.llm.openai_client import DummyLLMClient
from system.app.schemas.email_schemas import EmailCreateRequest
from system.app.repositories.email_repository import EmailRepository


class EmailClassificationService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        email_repository: EmailRepository | None = None,
    ):
        # Fallback para o cliente dummy quando não foi injetado.
        self._llm_client = llm_client or DummyLLMClient()
        self._email_repository = email_repository

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
            created_at=None,
            updated_at=None,
        )

        # chama a LLM
        result = await self._llm_client.classify_email(email)

        # preenche com resultado
        email.category = result.category
        email.confidence = result.confidence
        email.draft_reply = result.draft_reply
        email.requires_human_review = result.requires_human_review

        # salva no banco
        if self._email_repository is not None:
            email = self._email_repository.save(email)

        return email
