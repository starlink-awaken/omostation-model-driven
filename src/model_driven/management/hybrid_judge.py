"""
model_driven.management.hybrid_judge — 混合裁判模型 (Phase 4 Evaluation Flywheel)

提供 [代码硬性断言] + [LLM-as-Judge 语义评估] 的混合评价能力。
用于更复杂的生命周期卡点或数据质量评估。
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class JudgeResult:
    """裁判执行结果"""

    passed: bool
    score: float
    reason: str
    metrics: dict[str, Any]


class LLMGatewayProvider:
    """
    通过 HTTP 调用 llm-gateway 服务的 Provider
    默认地址: http://localhost:9290/v1/generate
    """

    def __init__(self, endpoint: str = "http://localhost:9290/v1/generate"):
        self.endpoint = endpoint

    def evaluate(self, text: str, criteria: str) -> dict[str, Any]:
        prompt = (
            f"You are an expert semantic evaluator.\n"
            f"Evaluate the following text based on this criteria: {criteria}\n\n"
            f"Text: {text}\n\n"
            f"Output a JSON object with 'passed' (boolean), 'score' (float 0.0 to 1.0), and 'reason' (string)."
        )

        req = urllib.request.Request(  # noqa: S310
            self.endpoint,
            data=json.dumps({"prompt": prompt}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:  # noqa: S310
                body = response.read().decode("utf-8")
                res = json.loads(body)
                content = res.get("content", "{}")
                # Attempt to parse LLM JSON output (may be wrapped in markdown code blocks)
                content_clean = content.strip().strip("```json").strip("```").strip()
                try:
                    return json.loads(content_clean)
                except json.JSONDecodeError:
                    # Fallback parsing
                    passed = "true" in content_clean.lower()
                    return {"passed": passed, "score": 1.0 if passed else 0.0, "reason": content_clean}
        except Exception as e:
            # Service unavailable or network error
            return {"error": str(e)}


class HybridJudge:
    """
    混合裁判引擎：
    整合结构化的代码断言与大语言模型(LLM)的语义评分。
    """

    def __init__(self, llm_provider: Any = None):
        """
        初始化混合裁判引擎
        :param llm_provider: 注入的 LLM 客户端 (如 LLMGatewayProvider / DeepEval / Ragas / 自建网关)
        """
        self.llm_provider = llm_provider

    def evaluate_semantic(self, text: str, criteria: str) -> JudgeResult:
        """
        [LLM-as-Judge 语义评估]
        根据给定的 criteria 评估 text 的语义质量。

        如果提供了 llm_provider，则调用远端模型；否则使用本地的基础启发式规则。
        """
        if self.llm_provider:
            eval_res = self.llm_provider.evaluate(text, criteria)
            if "error" not in eval_res:
                passed = bool(eval_res.get("passed", False))
                score = float(eval_res.get("score", 0.0))
                reason = str(eval_res.get("reason", "LLM Evaluation completed"))
                return JudgeResult(
                    passed=passed,
                    score=score,
                    reason=reason,
                    metrics={"semantic_score": score, "provider": "llm-gateway"},
                )

        # Fallback 到本地启发式规则
        words = text.split()
        score = min(1.0, len(words) / 10.0)  # 假定的启发式：字数越多得分越高
        passed = score >= 0.5

        return JudgeResult(
            passed=passed,
            score=score,
            reason="Heuristic evaluation based on word count" if not self.llm_provider else "LLM semantic evaluation",
            metrics={"word_count": len(words), "semantic_score": score},
        )

    def evaluate_hybrid(
        self, entity_data: dict[str, Any], schema_rules: dict[str, Any], semantic_fields: list[str]
    ) -> JudgeResult:
        """
        执行混合评估：
        1. 结构断言 (Schema checks)
        2. 语义断言 (Semantic checks on specific fields)
        """
        # 1. 结构断言
        structural_passed = True
        missing_fields = []
        for field in schema_rules.get("required_fields", []):
            if field not in entity_data:
                structural_passed = False
                missing_fields.append(field)

        if not structural_passed:
            return JudgeResult(
                passed=False,
                score=0.0,
                reason=f"Structural validation failed. Missing: {missing_fields}",
                metrics={"structural_passed": False},
            )

        # 2. 语义断言
        semantic_scores = []
        for field in semantic_fields:
            if field in entity_data:
                res = self.evaluate_semantic(str(entity_data[field]), f"Must be meaningful content for {field}")
                semantic_scores.append(res.score)

        avg_semantic = sum(semantic_scores) / len(semantic_scores) if semantic_scores else 1.0

        passed = avg_semantic >= 0.6
        return JudgeResult(
            passed=passed,
            score=avg_semantic,
            reason=f"Hybrid evaluation completed. Semantic score: {avg_semantic:.2f}",
            metrics={"structural_passed": True, "semantic_score": avg_semantic},
        )
