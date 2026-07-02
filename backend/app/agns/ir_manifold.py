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

def build_ir_from_contract(contract) -> IR8D:
    # TODO: real mapping logic
    return IR8D(
        x=0.0,
        y=0.0,
        z=0.0,
        semantic_intent=f"{contract.state}:{contract.shape}",
        confidence=contract.confidence,
        energy_level=contract.energy_level,
        ontological_persistence=0.5,
        policy_risk=0.1,
    )

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
