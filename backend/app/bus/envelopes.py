from dataclasses import dataclass
from typing import Any, Dict
import uuid
from datetime import datetime, timezone

@dataclass
class AkashicEnvelope:
    envelope_id: str
    intent_id: str
    session_id: str
    payload: Dict[str, Any]
    created_at: datetime

    @classmethod
    def from_payload(cls, *, intent_id: str, session_id: str, payload: Dict[str, Any]) -> "AkashicEnvelope":
        return cls(
            envelope_id=str(uuid.uuid4()),
            intent_id=intent_id,
            session_id=session_id,
            payload=payload,
            created_at=datetime.now(timezone.utc),
        )
