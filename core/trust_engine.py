from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TrustResult:
    score: float
    level: str
    deployment: str
    confidence: float
    breakdown: Dict
    recommendations: List[str]


class AITrustEngine:

    def __init__(self):
        self.weights = {
            "fairness": 0.20,
            "privacy": 0.20,
            "security": 0.15,
            "compliance": 0.20,
            "explainability": 0.15,
            "monitoring": 0.10,
        }

    def calculate(
        self,
        fairness=90,
        privacy=90,
        security=90,
        compliance=90,
        explainability=90,
        monitoring=90,
    ):

        weighted = (
            fairness * self.weights["fairness"]
            + privacy * self.weights["privacy"]
            + security * self.weights["security"]
            + compliance * self.weights["compliance"]
            + explainability * self.weights["explainability"]
            + monitoring * self.weights["monitoring"]
        )

        score = round(weighted, 1)

        if score >= 90:
            level = "Excellent"
            deployment = "APPROVED"

        elif score >= 75:
            level = "Good"
            deployment = "APPROVED WITH CONDITIONS"

        elif score >= 60:
            level = "Medium"
            deployment = "REVIEW REQUIRED"

        else:
            level = "Critical"
            deployment = "DO NOT DEPLOY"

        confidence = round(min(99.0, score + 5), 1)

        recommendations = []

        if fairness < 85:
            recommendations.append("Improve dataset fairness.")

        if privacy < 85:
            recommendations.append("Strengthen privacy safeguards.")

        if security < 85:
            recommendations.append("Perform security review.")

        if explainability < 85:
            recommendations.append("Generate SHAP explanations.")

        if compliance < 85:
            recommendations.append("Run compliance audit.")

        if monitoring < 85:
            recommendations.append("Enable continuous monitoring.")

        return TrustResult(
            score=score,
            level=level,
            deployment=deployment,
            confidence=confidence,
            breakdown={
                "Fairness": fairness,
                "Privacy": privacy,
                "Security": security,
                "Compliance": compliance,
                "Explainability": explainability,
                "Monitoring": monitoring,
            },
            recommendations=recommendations,
        )


if __name__ == "__main__":
    engine = AITrustEngine()

    result = engine.calculate(
        fairness=93,
        privacy=95,
        security=90,
        compliance=97,
        explainability=88,
        monitoring=92,
    )

    print(result)
