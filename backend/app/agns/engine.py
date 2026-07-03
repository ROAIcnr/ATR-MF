from typing import Dict, Any
from .dsl import extract_intent
from .morphology import MorphologyCompiler
from .governor import RuntimeGovernor, GovernorDecision

governor = RuntimeGovernor()
compiler = MorphologyCompiler()

async def process_intent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    :param payload: { raw_text, context_vector, emotional_valence, energy_level, ... }
    :return: validated Manifest Contract ready for frontend
    """
    # L2: AGNS - Intent Extraction -> AETH DSL
    dsl = extract_intent(payload)

    # L4: Morphology Compiler -> Manifest Contract
    contract = compiler.compile(dsl)

    # L5: Governor Verification - Patimokkha + clamping
    decision: GovernorDecision = governor.evaluate(contract)

    if decision.action in ("CLAMPED", "PASSED"):
        return {
            "contract": decision.contract,
            "governor_status": decision.action,
            "shannon_entropy": decision.shannon_entropy,
        }
    else:
        # NIRODHA or REJECTED ⇒ send safe void
        return {
            "contract": governor.safe_void_contract(),
            "governor_status": decision.action,
            "shannon_entropy": decision.shannon_entropy,
        }
