import pytest
from app.agns.governor import RuntimeGovernor, GovernorDecision
from app.agns.contract import ManifestContract
from app.agns.ir_manifold import IR8D

def create_mock_contract(energy_level=0.5, policy_risk=0.5) -> ManifestContract:
    ir = IR8D(
        x=0.0,
        y=0.0,
        z=0.0,
        semantic_intent="TEST",
        confidence=0.9,
        energy_level=energy_level,
        ontological_persistence=1.0,
        policy_risk=policy_risk
    )
    return ManifestContract(
        intent="TEST",
        archetype="DEFAULT_SPHERE",
        topology="BASIC_MESH",
        parameters={},
        ir=ir
    )

def test_governor_evaluate_passed():
    governor = RuntimeGovernor()
    contract = create_mock_contract(energy_level=0.5, policy_risk=0.5)

    decision = governor.evaluate(contract)

    assert decision.action == "PASSED"
    assert decision.contract["ir"]["energy_level"] == 0.5
    assert decision.contract["ir"]["policy_risk"] == 0.5
    assert decision.shannon_entropy > 0

def test_governor_evaluate_clamped_energy():
    governor = RuntimeGovernor()
    contract = create_mock_contract(energy_level=1.5, policy_risk=0.5)

    decision = governor.evaluate(contract)

    assert decision.action == "CLAMPED"
    assert decision.contract["ir"]["energy_level"] == 1.0
    assert decision.contract["ir"]["policy_risk"] == 0.5

def test_governor_evaluate_clamped_policy():
    governor = RuntimeGovernor()
    contract = create_mock_contract(energy_level=0.5, policy_risk=0.8)

    decision = governor.evaluate(contract)

    assert decision.action == "CLAMPED"
    assert decision.contract["ir"]["energy_level"] == 0.5
    assert decision.contract["ir"]["policy_risk"] == 0.7

def test_governor_evaluate_clamped_both():
    governor = RuntimeGovernor()
    contract = create_mock_contract(energy_level=1.5, policy_risk=0.8)

    decision = governor.evaluate(contract)

    assert decision.action == "CLAMPED"
    assert decision.contract["ir"]["energy_level"] == 1.0
    assert decision.contract["ir"]["policy_risk"] == 0.7

def test_governor_evaluate_nirodha():
    # Provide a very low entropy threshold so it easily triggers NIRODHA
    governor = RuntimeGovernor(entropy_threshold=-1.0)
    contract = create_mock_contract(energy_level=0.5, policy_risk=0.5)

    decision = governor.evaluate(contract)

    assert decision.action == "NIRODHA"
    assert decision.contract["ir"]["semantic_intent"] == "VOID"
    assert decision.contract["intent"] == "UNKNOWN"
