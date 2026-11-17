"""In-memory store for SNS login sessions and ready notifications."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from takeout_ordering.models import LoginResponse, NotifyReadyResponse

READY_NOTIFICATION_MESSAGE = "ご注文の品の準備が整いました"


class TakeoutStore:
    """In-memory storage for authentication sessions and order ready notifications."""

    def __init__(self) -> None:
        self.sessions: dict[str, LoginResponse] = {}
        self.notifications: list[dict[str, Any]] = []

    def create_session(
        self,
        provider: str,
        oauth_token: str,
        display_name: str,
    ) -> LoginResponse:
        """Issue and store a new SNS authentication session."""
        customer_id = f"cust-{provider}-{uuid4().hex[:8]}"
        access_token = f"tok-{uuid4().hex[:16]}"
        session = LoginResponse(
            customer_id=customer_id,
            provider=provider,
            display_name=display_name,
            access_token=access_token,
        )
        self.sessions[access_token] = session
        return session

    def record_ready_notification(self, order_id: str) -> NotifyReadyResponse:
        """Record an order-ready notification and return the response."""
        self.notifications.append(
            {
                "order_id": order_id,
                "message": READY_NOTIFICATION_MESSAGE,
                "notified_at": datetime.now(UTC).isoformat(),
            }
        )
        return NotifyReadyResponse(
            order_id=order_id,
            notified=True,
            message=READY_NOTIFICATION_MESSAGE,
        )
