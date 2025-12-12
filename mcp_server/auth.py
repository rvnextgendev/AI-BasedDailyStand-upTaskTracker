from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from jwt import InvalidTokenError
from .config import get_settings
from .schemas import UserContext

security = HTTPBearer(auto_error=True)


def _load_public_key(settings):
    if settings.JWT_PUBLIC_KEY:
        return settings.JWT_PUBLIC_KEY

    try:
        with open(settings.JWT_PUBLIC_KEY_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError("JWT public key not configured")


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> UserContext:
    settings = get_settings()
    token = creds.credentials
    public_key = _load_public_key(settings)

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except InvalidTokenError as ex:
        raise HTTPException(status_code=401, detail=f"Invalid token: {ex}")

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id or not role:
        raise HTTPException(status_code=401, detail="Token missing required claims")

    return UserContext(
        user_id=str(user_id),
        name=payload.get("name"),
        role=str(role),
    )
