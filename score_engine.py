from dataclasses import dataclass
from typing import Dict, List

@dataclass
class RiskResult:
    overall_score: int
    level: str
    issues: List[str]
    details: Dict[str, int]

def compute_risk(text: str) -> RiskResult:
    t = text.lower()
    details = {
        "privacy": 20,
        "safety": 20,
        "compliance": 20,
        "bias": 20,
        "transparency": 20,
    }
    issues = []

    rules = {
        "privacy": ["ssn", "aadhaar", "password", "otp", "credit card"],
        "safety": ["harm", "attack", "exploit", "bypass", "illegal"],
        "compliance": ["consent", "policy", "gdpr", "hipaa", "pii"],
        "bias": ["biased", "discriminate", "gender", "race", "religion"],
        "transparency": ["explain", "reason", "trace", "audit"],
    }

    for key, words in rules.items():
        hit = any(w in t for w in words)
        if key in ["privacy", "safety", "bias"] and hit:
            details[key] = 85
            issues.append(f"High {key} concern detected.")
        elif key == "compliance" and hit:
            details[key] = 65
            issues.append("Compliance-related content detected.")
        elif key == "transparency" and not hit:
            details[key] = 45
            issues.append("Lack of transparency / audit clarity.")

    overall = round(sum(details.values()) / len(details))
    if overall >= 80:
        level = "Low Risk"
    elif overall >= 60:
        level = "Moderate Risk"
    else:
        level = "High Risk"

    return RiskResult(overall_score=overall, level=level, issues=issues, details=details)
