from pydantic import BaseModel, EmailStr
from typing import Optional
from system.app.domain.entities.classification import EmailCategory


class EmailCreateRequest(BaseModel):
    from_email: EmailStr
    subject: str
    body: str


class EmailResponse(BaseModel):
    id: Optional[int] = None
    from_email: EmailStr
    subject: str
    body: str
    category: EmailCategory
    confidence: float
    draft_reply: str
    requires_human_review: bool