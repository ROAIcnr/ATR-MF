from dataclasses import dataclass
from typing import Literal, Dict, Any

State = Literal["IDLE", "THINKING", "RESPONDING"]
Shape = Literal["VORTEX", "SPHERE", "NEBULA"]

@dataclass
class AethContract:
    state: State
    shape: Shape
    flow: Literal["INWARD", "OUTWARD"]
    because: str
    confidence: float
    energy_level: float

def compile_aeth_contract(payload: Dict[str, Any]) -> AethContract:
    """
    Minimal IF-THEN-BECAUSE compiler skeleton.
    """
    state: State = payload.get("state", "THINKING")
    confidence = float(payload.get("confidence", 0.8))
    energy = float(payload.get("energy_level", 0.5))

    # demo rule: deep reasoning -> vortex inward
    if state == "THINKING":
        shape = "VORTEX"
        flow = "INWARD"
        because = "deep reasoning requires convergence"
    else:
        shape = "SPHERE"
        flow = "OUTWARD"
        because = "default expressive state"

    return AethContract(
        state=state,
        shape=shape,
        flow=flow,
        because=because,
        confidence=confidence,
        energy_level=energy,
    )
