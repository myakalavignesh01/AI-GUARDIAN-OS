"""
AI Guardian OS
Enterprise Deployment Decision Engine
Author : M. Vignesh
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DeploymentDecision:

    status: str
    confidence: float
    risk_level: str
    color: str
    reasons: List[str]
    required_actions: List[str]
    blockers: List[str]
    executive_summary: str


class DeploymentEngine:

    def __init__(self):

        self.high_risk_threshold = 60
        self.review_threshold = 75
        self.approval_threshold = 90

    def evaluate(self, trust_result):

        score = trust_result.score

        breakdown = trust_result.breakdown

        reasons = []

        blockers = []

        actions = []

        # ----------------------------------
        # FAIRNESS
        # ----------------------------------

        if breakdown["Fairness"] >= 90:
            reasons.append("Excellent fairness performance.")
        elif breakdown["Fairness"] >= 80:
            actions.append("Improve fairness before next release.")
        else:
            blockers.append("Fairness score too low.")

        # ----------------------------------
        # PRIVACY
        # ----------------------------------

        if breakdown["Privacy"] >= 90:
            reasons.append("Privacy controls verified.")
        elif breakdown["Privacy"] >= 80:
            actions.append("Review privacy safeguards.")
        else:
            blockers.append("Privacy compliance failed.")

        # ----------------------------------
        # SECURITY
        # ----------------------------------

        if breakdown["Security"] >= 90:
            reasons.append("Security assessment passed.")
        elif breakdown["Security"] >= 80:
            actions.append("Perform penetration testing.")
        else:
            blockers.append("Security score below policy.")

        # ----------------------------------
        # COMPLIANCE
        # ----------------------------------

        if breakdown["Compliance"] >= 90:
            reasons.append("Regulatory compliance verified.")
        elif breakdown["Compliance"] >= 80:
            actions.append("Complete compliance review.")
        else:
            blockers.append("Compliance requirements not met.")

        # ----------------------------------
        # EXPLAINABILITY
        # ----------------------------------

        if breakdown["Explainability"] >= 90:
            reasons.append("Model is explainable.")
        elif breakdown["Explainability"] >= 80:
            actions.append("Generate SHAP report.")
        else:
            blockers.append("Model explainability insufficient.")

        # ----------------------------------
        # MONITORING
        # ----------------------------------

        if breakdown["Monitoring"] >= 90:
            reasons.append("Continuous monitoring enabled.")
        elif breakdown["Monitoring"] >= 80:
            actions.append("Increase monitoring coverage.")
        else:
            blockers.append("Monitoring not configured.")

        # ----------------------------------
        # DECISION LOGIC
        # ----------------------------------

        if len(blockers) > 0:

            status = "DO NOT DEPLOY"

            color = "red"

            risk = "Critical"

            confidence = 98.0

        elif score >= self.approval_threshold:

            status = "APPROVED"

            color = "green"

            risk = "Low"

            confidence = 97.5

        elif score >= self.review_threshold:

            status = "APPROVED WITH CONDITIONS"

            color = "orange"

            risk = "Medium"

            confidence = 94.0

        else:

            status = "REVIEW REQUIRED"

            color = "orange"

            risk = "Medium"

            confidence = 90.0

        # ----------------------------------
        # EXECUTIVE SUMMARY
        # ----------------------------------

        summary = f"""
Deployment Recommendation

Status : {status}

Overall Trust Score : {score}

Risk Level : {risk}

Confidence : {confidence}%

Business Recommendation

Deploy only after completing required governance actions.

AI Guardian OS recommends continuous monitoring
after production deployment.
"""

        return DeploymentDecision(

            status=status,

            confidence=confidence,

            risk_level=risk,

            color=color,

            reasons=reasons,

            required_actions=actions,

            blockers=blockers,

            executive_summary=summary,
        )
