from fastapi import Depends
from sqlalchemy.orm import Session

from system.app.infrastructure.db.session import get_db
from system.app.repositories.email_repository import (
    SqlAlchemyEmailRepository,
    EmailRepository,
)
from system.app.services.email_service import EmailClassificationService
from system.app.core.config import settings
from system.app.infrastructure.llm.llm_client import LLMClient
from system.app.infrastructure.llm.openai_client import DummyLLMClient


def get_email_repository(db: Session = Depends(get_db)) -> EmailRepository:
    return SqlAlchemyEmailRepository(db)


def get_email_classification_service(
    repo: EmailRepository = Depends(get_email_repository),
) -> EmailClassificationService:
    llm_client = LLMClient() if settings.OPENAI_API_KEY else DummyLLMClient()
    return EmailClassificationService(
        llm_client=llm_client,
        email_repository=repo,
    )
