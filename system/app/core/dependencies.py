# system/app/core/dependencies.py
from system.app.services.email_service import EmailClassificationService


def get_email_classification_service() -> EmailClassificationService:
    return EmailClassificationService()