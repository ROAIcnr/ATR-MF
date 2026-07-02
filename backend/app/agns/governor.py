from dataclasses import dataclass
from typing import Literal, Dict, Any
from .ir_manifold import IR8D, ir_to_dict
from .contract import ManifestContract, contract_to_dict
import math

Action = Literal["PASSED", "CLAMPED", "REJECTED", "NIRODHA"]

@dataclass
class GovernorDecision:
    action: Action
    contract: dict
    shannon_entropy: float

class RuntimeGovernor:
    def __init__(self, entropy_threshold: float = 1.58):
        self.entropy_threshold = entropy_threshold

    def evaluate(self, contract: ManifestContract) -> GovernorDecision:
        ir = contract.ir

        # placeholder entropy: function of energy + policy_risk
        shannon_entropy = self._approx_entropy(ir)

        contract_dict = contract_to_dict(contract)
        ir_dict = contract_dict["ir"]

        # clamp dangerous params
        clamped = False
        if ir_dict["energy_level"] > 1.0:
            ir_dict["energy_level"] = 1.0
            clamped = True
        if ir_dict["policy_risk"] > 0.7:
            ir_dict["policy_risk"] = 0.7
            clamped = True

        contract_dict["ir"] = ir_dict

        if shannon_entropy > self.entropy_threshold:
            return GovernorDecision(action="NIRODHA", contract=self.safe_void_contract(), shannon_entropy=shannon_entropy)

        if clamped:
            return GovernorDecision(action="CLAMPED", contract=contract_dict, shannon_entropy=shannon_entropy)

        return GovernorDecision(action="PASSED", contract=contract_dict, shannon_entropy=shannon_entropy)

    def safe_void_contract(self) -> dict:
        ir_dict = {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "semantic_intent": "VOID",
            "confidence": 0.0,
            "energy_level": 0.0,
            "ontological_persistence": 1.0,
            "policy_risk": 0.0,
            "color": "#0B1026",
        }

        return {
            "intent": "UNKNOWN",
            "archetype": "DEFAULT_SPHERE",
            "topology": "BASIC_MESH",
            "parameters": {},
            "ir": ir_dict
        }

    def _approx_entropy(self, ir: IR8D) -> float:
        # toy entropy approximation
        e = max(0.0001, ir.energy_level)
        return -e * math.log2(e)
