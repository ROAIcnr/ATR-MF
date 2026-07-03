from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class IR8D:
    x: float
    y: float
    z: float
    semantic_intent: str
    confidence: float
    energy_level: float
    ontological_persistence: float
    policy_risk: float

def ir_to_dict(ir: IR8D) -> Dict[str, Any]:
    return {
        "x": ir.x,
        "y": ir.y,
        "z": ir.z,
        "semantic_intent": ir.semantic_intent,
        "confidence": ir.confidence,
        "energy_level": ir.energy_level,
        "ontological_persistence": ir.ontological_persistence,
        "policy_risk": ir.policy_risk,
    }
