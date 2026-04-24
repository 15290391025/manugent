"""Minimal API-token helper.

This is intentionally not a full enterprise identity system. In production,
ManuGent should normally sit behind SSO/API Gateway/IAM. The token guard is a
small local safeguard for demos and direct deployments.
"""

from __future__ import annotations

import secrets


def verify_bearer_token(authorization: str | None, expected_token: str) -> bool:
    """Verify an Authorization: Bearer token header."""
    if not expected_token:
        return True
    if not authorization:
        return False

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return False
    return secrets.compare_digest(token, expected_token)
