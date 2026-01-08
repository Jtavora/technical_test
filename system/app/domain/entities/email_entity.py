from dataclasses import dataclass
from typing import Optional

from system.app.domain.entities.classification import EmailCategory


@dataclass
class Email:
    id: Optional[int]
    from_email: str
    subject: str
    body: str
    category: EmailCategory
    confidence: float
    draft_reply: str
    requires_human_review: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None