from typing import Dict, Any
from .aeth_contract import compile_aeth_contract
from .ir_manifold import build_ir_from_contract
from .governor import RuntimeGovernor, GovernorDecision

governor = RuntimeGovernor()

async def process_intent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    :param payload: { raw_text, context_vector, emotional_valence, energy_level, ... }
    :return: validated 8D IR ready for frontend
    """
    # L2: AGNS – parse + MRDE placeholder
    # TODO: implement MRDE; currently pass-through with basic fields
    contract = compile_aeth_contract(payload)

    # L4: IR – 8D canonical representation
    ir = build_ir_from_contract(contract)

    # L5: Governor – Patimokkha + clamping
    decision: GovernorDecision = governor.evaluate(ir)

    if decision.action in ("CLAMPED", "PASSED"):
        return {
            "ir": decision.ir,
            "governor_status": decision.action,
            "shannon_entropy": decision.shannon_entropy,
        }
    else:
        # NIRODHA or REJECTED ⇒ send safe void
        return {
            "ir": governor.safe_void(),
            "governor_status": decision.action,
            "shannon_entropy": decision.shannon_entropy,
        }
