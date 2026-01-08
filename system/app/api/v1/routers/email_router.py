# system/app/api/v1/routers/email_router.py
from fastapi import APIRouter, Depends

from system.app.schemas.email_schemas import EmailCreateRequest, EmailResponse
from system.app.services.email_service import EmailClassificationService
from system.app.core.dependencies import get_email_classification_service

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/classify", response_model=EmailResponse)
async def classify_email(
    payload: EmailCreateRequest,
    service: EmailClassificationService = Depends(get_email_classification_service),
):
    email = await service.classify_from_request(payload)
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