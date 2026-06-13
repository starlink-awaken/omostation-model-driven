"""
Tests for Hybrid Judge.
"""

from model_driven.management.hybrid_judge import HybridJudge


def test_hybrid_judge_semantic_fallback():
    judge = HybridJudge()
    res = judge.evaluate_semantic("This is a sufficiently long text for the semantic check to pass.", "test")
    assert res.passed
    assert res.score > 0.5

    res_fail = judge.evaluate_semantic("Too short", "test")
    assert not res_fail.passed
    assert res_fail.score < 0.5


def test_hybrid_judge_hybrid_evaluation():
    judge = HybridJudge()

    entity = {
        "id": "E-01",
        "description": "This is a detailed description of the model entity, which explains its purpose and usage.",
    }

    schema = {"required_fields": ["id", "description"]}

    res = judge.evaluate_hybrid(entity, schema, semantic_fields=["description"])

    assert res.passed
    assert res.metrics["structural_passed"] is True
    assert res.metrics["semantic_score"] > 0.5


def test_hybrid_judge_hybrid_evaluation_fail_structural():
    judge = HybridJudge()
    entity = {"id": "E-01"}
    schema = {"required_fields": ["id", "description"]}

    res = judge.evaluate_hybrid(entity, schema, semantic_fields=["description"])

    assert not res.passed
    assert res.metrics["structural_passed"] is False
    assert res.score == 0.0
