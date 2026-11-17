"""Pydantic models for takeout ordering API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SnsProvider = Literal["google", "facebook", "line"]


class LoginRequest(BaseModel):
    """Request payload for SNS login."""

    provider: SnsProvider
    oauth_token: str = Field(min_length=1)
    display_name: str = "Guest"


class LoginResponse(BaseModel):
    """Response payload for SNS login."""

    customer_id: str
    provider: str
    display_name: str
    access_token: str


class OrderItemInput(BaseModel):
    """Order line item input for takeout orders."""

    model_config = ConfigDict(extra="allow")

    product_id: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1)


class TakeoutOrderRequest(BaseModel):
    """Request payload for creating a takeout order with pickup time."""

    customer_id: str = Field(min_length=1)
    pickup_at: str = Field(min_length=1)
    items: list[OrderItemInput] = Field(min_length=1)


class NotifyReadyResponse(BaseModel):
    """Response payload for order ready notification."""

    order_id: str
    notified: bool
    message: str
