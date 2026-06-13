"""
Evaluation Flywheel for model-driven elements (Phase 4).
Integrates with X1-X4 governance.
"""

from typing import Any

from model_driven.management.omo_bridge import OMOBridge


class GovernanceEvaluator:
    """
    Evaluator that assesses model-driven entities against X1-X4 constraints.
    - X1 (Audit): checks for trace/history
    - X2 (Freshness): checks for recent updates
    - X3 (Value): checks for goal/value linkage
    - X4 (Consistency): checks for schema validity
    """
    def __init__(self, omo_bridge: OMOBridge = None):
        self.results = []
        self.bridge = omo_bridge or OMOBridge()

    def evaluate_entity(self, entity_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Evaluate a single entity."""
        # X1: Audit check (has history/traceability)
        x1_pass = "history" in data or "audit" in data or "trace_id" in data

        # X2: Freshness check (recently updated)
        x2_pass = "updated_at" in data or "last_modified" in data

        # X3: Value stack (linked to goals/values)
        x3_pass = "value_link" in data or "goal_id" in data or "value" in data

        # X4: Consistency (schema valid)
        x4_pass = "type" in data and "id" in data and data["id"] == entity_id

        score = sum([x1_pass, x2_pass, x3_pass, x4_pass]) / 4.0

        result = {
            "entity_id": entity_id,
            "x1_audit": x1_pass,
            "x2_freshness": x2_pass,
            "x3_value": x3_pass,
            "x4_consistency": x4_pass,
            "score": score
        }
        self.results.append(result)

        # OMO Bridge Integration (Phase 4 Flywheel)
        self.bridge.record_audit(
            action="evaluate_x1_x4",
            entity_type=data.get("type", "unknown"),
            entity_id=entity_id,
            details=result
        )

        if score < 1.0:
            failed_checks = []
            if not x1_pass:
                failed_checks.append("X1")
            if not x2_pass:
                failed_checks.append("X2")
            if not x3_pass:
                failed_checks.append("X3")
            if not x4_pass:
                failed_checks.append("X4")

            self.bridge.register_debt(
                title=f"Entity {entity_id} fails X1-X4 compliance",
                description=f"Failed checks: {', '.join(failed_checks)}. Score: {score}",
                severity="high" if score <= 0.5 else "medium",
                source="model-driven-evaluator"
            )

        return result

    def get_aggregate_report(self) -> dict[str, Any]:
        """Generate a summarized report of all evaluations."""
        if not self.results:
            return {"total_evaluated": 0, "average_score": 0.0}

        avg_score = sum(r["score"] for r in self.results) / len(self.results)

        return {
            "total_evaluated": len(self.results),
            "average_score": avg_score,
            "x1_pass_rate": sum(1 for r in self.results if r["x1_audit"]) / len(self.results),
            "x2_pass_rate": sum(1 for r in self.results if r["x2_freshness"]) / len(self.results),
            "x3_pass_rate": sum(1 for r in self.results if r["x3_value"]) / len(self.results),
            "x4_pass_rate": sum(1 for r in self.results if r["x4_consistency"]) / len(self.results),
        }
