"""
Tests for the Phase 4 Governance Evaluator.
"""

from model_driven.management.evaluator import GovernanceEvaluator
from model_driven.management.omo_bridge import OMOBridge


def test_governance_evaluator_perfect_entity():
    bridge = OMOBridge()
    evaluator = GovernanceEvaluator(omo_bridge=bridge)

    entity = {
        "id": "E-PERFECT",
        "type": "M2_Entity",
        "history": ["creation_event"],
        "updated_at": "now",
        "value_link": "demo_goal",
    }

    result = evaluator.evaluate_entity("E-PERFECT", entity)

    assert result["x1_audit"] is True
    assert result["x2_freshness"] is True
    assert result["x3_value"] is True
    assert result["x4_consistency"] is True
    assert result["score"] == 1.0


def test_governance_evaluator_failing_entity():
    bridge = OMOBridge()
    evaluator = GovernanceEvaluator(omo_bridge=bridge)

    # Missing history (X1), updated_at (X2), value_link (X3)
    entity = {"id": "E-FAIL", "type": "M2_Entity"}

    result = evaluator.evaluate_entity("E-FAIL", entity)

    assert result["x1_audit"] is False
    assert result["x2_freshness"] is False
    assert result["x3_value"] is False
    assert result["x4_consistency"] is True  # id and type are present
    assert result["score"] == 0.25

    # Check if a debt was registered via the bridge
    assert len(bridge._pending_debts) == 1
    debt = bridge._pending_debts[0]
    assert "E-FAIL" in debt["title"]
    assert "X1" in debt["description"]
    assert "X2" in debt["description"]
    assert "X3" in debt["description"]


def test_aggregate_report():
    evaluator = GovernanceEvaluator()

    evaluator.evaluate_entity("E1", {"id": "E1", "type": "T", "history": [], "updated_at": "", "value_link": ""})
    evaluator.evaluate_entity("E2", {"id": "E2", "type": "T"})

    report = evaluator.get_aggregate_report()
    assert report["total_evaluated"] == 2
    assert report["average_score"] == 0.625
