from typing import Optional

from pydantic import BaseModel, EmailStr

from system.app.domain.entities.classification import EmailCategory


class EmailCreateRequest(BaseModel):
    from_email: EmailStr
    subject: str
    body: str


class EmailUpdateRequest(BaseModel):
    draft_reply: Optional[str] = None
    category: Optional[EmailCategory] = None
    requires_human_review: Optional[bool] = None
    confidence: Optional[float] = None


class EmailResponse(BaseModel):
    id: Optional[int] = None
    from_email: EmailStr
    subject: str
    body: str
    category: EmailCategory
    confidence: float
    draft_reply: str
    requires_human_review: bool