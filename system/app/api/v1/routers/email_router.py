from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from system.app.schemas.email_schemas import (
    EmailCreateRequest,
    EmailResponse,
    EmailUpdateRequest,
)
from system.app.services.email_service import EmailClassificationService
from system.app.core.dependencies import (
    get_email_classification_service,
    get_email_repository,
)
from system.app.repositories.email_repository import EmailRepository

router = APIRouter(prefix="/emails", tags=["emails"])


def _to_response(email) -> EmailResponse:
    return EmailResponse(
        id=email.id,
        from_email=email.from_email,
        subject=email.subject,
        body=email.body,
        category=email.category,
        confidence=email.confidence,
        draft_reply=email.draft_reply,
        requires_human_review=email.requires_human_review,
    )


@router.post("/classify", response_model=EmailResponse)
async def classify_email(
    payload: EmailCreateRequest,
    service: EmailClassificationService = Depends(get_email_classification_service),
):
    email = await service.classify_from_request(payload)
    return _to_response(email)


@router.get("/", response_model=List[EmailResponse])
def list_emails(
    repo: EmailRepository = Depends(get_email_repository),
):
    emails = repo.list()
    return [_to_response(e) for e in emails]


@router.get("/{email_id}", response_model=EmailResponse)
def get_email(
    email_id: int,
    repo: EmailRepository = Depends(get_email_repository),
):
    email = repo.get(email_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado",
        )
    return _to_response(email)


@router.put("/{email_id}", response_model=EmailResponse)
def update_email(
    email_id: int,
    payload: EmailUpdateRequest,
    repo: EmailRepository = Depends(get_email_repository),
):
    email = repo.get(email_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado",
        )

    if payload.draft_reply is not None:
        email.draft_reply = payload.draft_reply
    if payload.category is not None:
        email.category = payload.category
    if payload.requires_human_review is not None:
        email.requires_human_review = payload.requires_human_review
    if payload.confidence is not None:
        email.confidence = payload.confidence

    email = repo.save(email)
    return _to_response(email)