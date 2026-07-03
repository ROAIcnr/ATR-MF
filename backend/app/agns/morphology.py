from typing import Tuple, Dict, Any
from .dsl import AethDSL
from .contract import ManifestContract, Archetype, Topology
from .ir_manifold import IR8D

class MorphologyCompiler:
    """
    Compiles AethDSL into a ManifestContract via three steps:
    1. Archetype Selection
    2. Topology Resolution
    3. Parameter Synthesis
    """

    def compile(self, dsl: AethDSL) -> ManifestContract:
        archetype = self._select_archetype(dsl)
        topology = self._resolve_topology(dsl, archetype)
        parameters = self._synthesize_parameters(dsl, archetype, topology)

        # Build 8D IR from synthesized parameters
        ir = self._build_ir(dsl, archetype, topology, parameters)

        return ManifestContract(
            intent=dsl.intent,
            archetype=archetype,
            topology=topology,
            parameters=parameters,
            ir=ir
        )

    def _select_archetype(self, dsl: AethDSL) -> Archetype:
        if dsl.intent == "TREE":
            return "ARBOR"
        elif dsl.intent == "VORTEX":
            return "VORTEX_CORE"
        elif dsl.intent == "SHELL":
            return "CRACKED_SHELL"
        return "DEFAULT_SPHERE"

    def _resolve_topology(self, dsl: AethDSL, archetype: Archetype) -> Topology:
        if archetype == "ARBOR":
            # Just an example logic for choosing topology based on DSL parameters
            if dsl.energy_level > 0.8:
                return "MULTI_TRUNK"
            return "TRUNK_BRANCH_LEAF"
        elif archetype == "VORTEX_CORE":
            if dsl.energy_level < 0.3:
                return "INWARD_COLLAPSE"
            return "SPIRAL_ARMS"
        elif archetype == "CRACKED_SHELL":
            return "FRACTURE_LINES"
        return "BASIC_MESH"

    def _synthesize_parameters(self, dsl: AethDSL, archetype: Archetype, topology: Topology) -> Dict[str, Any]:
        params = {
            "scale": dsl.energy_level * 10,
            "density": dsl.confidence * 5
        }

        if archetype == "ARBOR":
            params["branching_factor"] = 3 if topology == "TRUNK_BRANCH_LEAF" else 5
        elif archetype == "VORTEX_CORE":
            params["rotation_speed"] = dsl.energy_level * 5.0

        return params

    def _build_ir(self, dsl: AethDSL, archetype: Archetype, topology: Topology, parameters: Dict[str, Any]) -> IR8D:
        return IR8D(
            x=0.0,
            y=0.0,
            z=0.0,
            semantic_intent=f"{dsl.intent}:{archetype}:{topology}",
            confidence=dsl.confidence,
            energy_level=dsl.energy_level,
            ontological_persistence=0.5,
            policy_risk=0.1,
        )
