"""
Notification Service.

Handles dispatch of notifications to various channels (Email, SMS, Slack, etc.).
Implements the Strategy Pattern for extensible notification backends.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    SLACK = "SLACK"
    WEBHOOK = "WEBHOOK"
    IN_APP = "IN_APP"


class NotificationPayload(BaseModel):
    """Content of a notification."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str
    body: str
    recipient: str
    channel: NotificationChannel
    created_at: datetime = Field(default_factory=datetime.now)
    sent_at: Optional[datetime] = None
    metadata: dict = {}


class NotificationBackend(ABC):
    """Interface for notification delivery backends (Strategy Pattern)."""
    
    @abstractmethod
    def send(self, payload: NotificationPayload) -> bool:
        """Sends the notification. Returns True if successful."""
        pass


class EmailBackend(NotificationBackend):
    """Simulated email sender."""
    
    def send(self, payload: NotificationPayload) -> bool:
        # In production, integrate with SMTP or SendGrid/SES
        print(f"[EMAIL] To: {payload.recipient} | Subject: {payload.subject}")
        payload.sent_at = datetime.now()
        return True


class SlackBackend(NotificationBackend):
    """Simulated Slack webhook sender."""
    
    def send(self, payload: NotificationPayload) -> bool:
        # In production, use Slack Webhook API
        print(f"[SLACK] Channel: {payload.recipient} | Message: {payload.body[:50]}...")
        payload.sent_at = datetime.now()
        return True


class InAppBackend(NotificationBackend):
    """In-application notification storage."""
    
    def __init__(self):
        self._inbox: List[NotificationPayload] = []
    
    def send(self, payload: NotificationPayload) -> bool:
        payload.sent_at = datetime.now()
        self._inbox.append(payload)
        return True
    
    def get_inbox(self, user_id: str) -> List[NotificationPayload]:
        return [n for n in self._inbox if n.recipient == user_id]


class NotificationService:
    """
    Central service for dispatching notifications.
    Routes to the appropriate backend based on channel.
    """
    
    def __init__(self):
        self._backends = {
            NotificationChannel.EMAIL: EmailBackend(),
            NotificationChannel.SLACK: SlackBackend(),
            NotificationChannel.IN_APP: InAppBackend(),
        }
        self._history: List[NotificationPayload] = []
    
    def register_backend(self, channel: NotificationChannel, backend: NotificationBackend):
        """Allows custom backends to be injected (Dependency Injection)."""
        self._backends[channel] = backend
    
    def send(self, payload: NotificationPayload) -> bool:
        """Dispatches a notification through the appropriate channel."""
        backend = self._backends.get(payload.channel)
        if not backend:
            print(f"[WARN] No backend registered for channel: {payload.channel}")
            return False
        
        success = backend.send(payload)
        self._history.append(payload)
        return success
    
    def broadcast(self, subject: str, body: str, recipients: List[str], channel: NotificationChannel) -> int:
        """Sends the same notification to multiple recipients. Returns count of successful sends."""
        success_count = 0
        for recipient in recipients:
            payload = NotificationPayload(
                subject=subject,
                body=body,
                recipient=recipient,
                channel=channel
            )
            if self.send(payload):
                success_count += 1
        return success_count
    
    def get_history(self, limit: int = 100) -> List[NotificationPayload]:
        """Returns the most recent notifications."""
        return self._history[-limit:]


# Singleton instance
notification_service = NotificationService()
