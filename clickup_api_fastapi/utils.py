
from fastapi import status, HTTPException
from .enums import Static


def header(token: str | None = None, content_type: str | None = None) -> dict:
    if not token:
        token = Static.TOKEN.value
    if not content_type:
        content_type = "application/json"
    return {"Authorization": token, "Content-Type": content_type}


def validate_token(token: str | None) -> bool:
    if not token:
        try:
            token = Static.TOKEN.value
        except AttributeError:
            token = None
    if not token or token == "None":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found / invalid token.")
