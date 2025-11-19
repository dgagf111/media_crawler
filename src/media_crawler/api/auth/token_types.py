from __future__ import annotations

from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    PERMANENT = "permanent"

    @classmethod
    def from_payload(cls, payload: dict) -> "TokenType":
        raw_type = payload.get("type", cls.ACCESS.value)
        try:
            return cls(raw_type)
        except ValueError:
            return cls.ACCESS
