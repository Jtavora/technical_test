from typing import Protocol, Optional, List

from sqlalchemy.orm import Session

from system.app.domain.entities.email_entity import Email
from system.app.domain.entities.classification import EmailCategory
from system.app.infrastructure.db.models.email_model import EmailModel


class EmailRepository(Protocol):
    def save(self, email: Email) -> Email: ...
    def get(self, email_id: int) -> Optional[Email]: ...
    def list(self) -> List[Email]: ...


class SqlAlchemyEmailRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, email: Email) -> Email:
        if email.id is None:
            model = EmailModel(
                from_email=email.from_email,
                subject=email.subject,
                body=email.body,
                category=email.category.value,
                confidence=email.confidence,
                draft_reply=email.draft_reply,
                requires_human_review=email.requires_human_review,
            )
            self._session.add(model)
            self._session.commit()
            self._session.refresh(model)
            email.id = model.id
        else:
            model = self._session.get(EmailModel, email.id)
            if not model:
                raise ValueError(f"Email id={email.id} não encontrado")

            model.category = email.category.value
            model.confidence = email.confidence
            model.draft_reply = email.draft_reply
            model.requires_human_review = email.requires_human_review

            self._session.commit()
            self._session.refresh(model)

        return email

    def get(self, email_id: int) -> Optional[Email]:
        model = self._session.get(EmailModel, email_id)
        if not model:
            return None
        return self._to_entity(model)

    def list(self) -> list[Email]:
        models = (
            self._session.query(EmailModel)
            .order_by(EmailModel.created_at.desc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: EmailModel) -> Email:
        return Email(
            id=model.id,
            from_email=model.from_email,
            subject=model.subject,
            body=model.body,
            category=EmailCategory(model.category),
            confidence=model.confidence,
            draft_reply=model.draft_reply,
            requires_human_review=model.requires_human_review,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )