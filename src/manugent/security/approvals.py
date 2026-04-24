"""Human approval queue for safety-gated manufacturing actions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


class ApprovalStatus(StrEnum):
    """Approval lifecycle states."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    """A safety-gated tool request awaiting human decision."""

    tool_name: str
    params: dict[str, Any]
    safety_level: str
    session_id: str = "default"
    request_id: str = field(default_factory=lambda: uuid4().hex)
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "tool_name": self.tool_name,
            "params": self.params,
            "safety_level": self.safety_level,
            "session_id": self.session_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "reason": self.reason,
        }


@dataclass
class ApprovalDecision:
    """A human approval or rejection."""

    request_id: str
    approved: bool
    decided_by: str = "human"
    reason: str = ""


class ApprovalQueue:
    """In-memory approval queue.

    This queue is a skeleton for demos. Enterprise deployments should wire the
    same object model to workflow tools such as ServiceNow, Jira, MES approval
    screens, Teams/Slack, or customer-specific approval systems.
    """

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}

    def submit(self, request: ApprovalRequest) -> ApprovalRequest:
        self._requests[request.request_id] = request
        return request

    def get(self, request_id: str) -> ApprovalRequest | None:
        return self._requests.get(request_id)

    def list_pending(self, session_id: str | None = None) -> list[ApprovalRequest]:
        requests = [
            request
            for request in self._requests.values()
            if request.status == ApprovalStatus.PENDING
        ]
        if session_id is not None:
            requests = [request for request in requests if request.session_id == session_id]
        return sorted(requests, key=lambda request: request.created_at)

    def decide(self, decision: ApprovalDecision) -> ApprovalRequest | None:
        request = self._requests.get(decision.request_id)
        if request is None:
            return None
        request.status = ApprovalStatus.APPROVED if decision.approved else ApprovalStatus.REJECTED
        request.reason = decision.reason
        return request
