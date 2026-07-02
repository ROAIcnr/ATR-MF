from dataclasses import dataclass, asdict
from typing import Dict, Any, Literal
from .ir_manifold import IR8D

Archetype = Literal["ARBOR", "VORTEX_CORE", "CRACKED_SHELL", "DEFAULT_SPHERE"]
Topology = Literal["TRUNK_BRANCH_LEAF", "MULTI_TRUNK", "SPIRAL_ARMS", "INWARD_COLLAPSE", "FRACTURE_LINES", "BASIC_MESH"]

@dataclass
class ManifestContract:
    """
    Executable Runtime Contract.
    Output of the Morphology Compiler, ready for Governor and Renderer.
    """
    intent: str
    archetype: Archetype
    topology: Topology
    parameters: Dict[str, Any]
    ir: IR8D

def contract_to_dict(contract: ManifestContract) -> Dict[str, Any]:
    return {
        "intent": contract.intent,
        "archetype": contract.archetype,
        "topology": contract.topology,
        "parameters": contract.parameters,
        "ir": asdict(contract.ir)
    }
