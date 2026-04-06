import logging
from typing import Optional

import jwt

from app.core.config import settings

logger = logging.getLogger(__name__)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        return None


def authenticate(token: str) -> Optional[dict]:
    if not token:
        return None

    payload = decode_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id:
        return None

    if role not in settings.JWT_ALLOWED_ROLES:
        return None

    return {"user_id": user_id, "role": role}
