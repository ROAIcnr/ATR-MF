from dataclasses import dataclass
from typing import Dict, Any, Literal

Intent = Literal["TREE", "VORTEX", "SPHERE", "SHELL", "UNKNOWN"]

@dataclass
class AethDSL:
    """
    Declarative Specification of Intent.
    Tells "what" is needed and "why", but not "how".
    """
    intent: Intent
    because: str
    confidence: float
    energy_level: float

def extract_intent(payload: Dict[str, Any]) -> AethDSL:
    """
    L2 AGNS: Captures latent intent from payload (text/signal).
    """
    # Placeholder for more complex intent extraction
    raw_intent = payload.get("intent", "UNKNOWN").upper()
    intent: Intent = raw_intent if raw_intent in ["TREE", "VORTEX", "SPHERE", "SHELL"] else "UNKNOWN"

    confidence = float(payload.get("confidence", 0.8))
    energy_level = float(payload.get("energy_level", 0.5))
    because = payload.get("because", "user request inferred")

    return AethDSL(
        intent=intent,
        because=because,
        confidence=confidence,
        energy_level=energy_level,
    )
