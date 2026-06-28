import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import json

@dataclass
class TrustResult:
    score: float
    level: str
    deployment: str
    confidence: float
    breakdown: Dict
    recommendations: List[str]
    timestamp: str

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
        self.history = []

    def calculate(self, **kwargs):
        values = {k: kwargs.get(k, 90) for k in self.weights.keys()}

        weighted = sum(values[k] * self.weights[k] for k in self.weights)
        score = round(weighted, 1)

        if score >= 90:
            level, deployment, color = "Excellent", "✅ APPROVED", "green"
        elif score >= 75:
            level, deployment, color = "Good", "🟡 APPROVED WITH CONDITIONS", "orange"
        elif score >= 60:
            level, deployment, color = "Medium", "🔶 REVIEW REQUIRED", "red"
        else:
            level, deployment, color = "Critical", "❌ DO NOT DEPLOY", "darkred"

        confidence = round(min(99.0, score + 5), 1)

        rec_map = {
            "fairness": "Improve dataset fairness and reduce bias.",
            "privacy": "Strengthen privacy safeguards and data protection.",
            "security": "Perform thorough security review and testing.",
            "compliance": "Run full compliance and regulatory audit.",
            "explainability": "Generate SHAP/LIME explanations and documentation.",
            "monitoring": "Enable continuous monitoring and drift detection.",
        }
        recommendations = [rec_map[k] for k, v in values.items() if v < 85]

        result = TrustResult(
            score=score,
            level=level,
            deployment=deployment,
            confidence=confidence,
            breakdown=values,
            recommendations=recommendations,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        self.history.append(result)
        return result


# ====================== STREAMLIT APP ======================
st.set_page_config(page_title="AI Trust Copilot", page_icon="🤖", layout="wide")

st.title("🤖 AI Trust Copilot")
st.markdown("**100x Hackathon Edition** — Real-time AI Trust Assessment")

# Initialize engine in session state
if 'engine' not in st.session_state:
    st.session_state.engine = AITrustEngine()

engine = st.session_state.engine

# Sidebar Controls
with st.sidebar:
    st.header("🔧 Live Assessment Controls")
    
    col_a, col_b = st.columns(2)
    with col_a:
        fairness = st.slider("Fairness", 0, 100, 93, help="Bias detection & equity")
        privacy = st.slider("Privacy", 0, 100, 95, help="Data protection & consent")
        security = st.slider("Security", 0, 100, 90, help="Adversarial robustness")
    with col_b:
        compliance = st.slider("Compliance", 0, 100, 97, help="Regulatory & legal alignment")
        explainability = st.slider("Explainability", 0, 100, 88, help="Model interpretability")
        monitoring = st.slider("Monitoring", 0, 100, 92, help="Drift detection & observability")

    st.divider()
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        st.session_state.engine = AITrustEngine()
        st.rerun()

# Calculate result
result = engine.calculate(
    fairness=fairness,
    privacy=privacy,
    security=security,
    compliance=compliance,
    explainability=explainability,
    monitoring=monitoring
)

# Main Content
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Overall Trust Result")
    st.markdown(f"""
    <div style="padding: 25px; border-radius: 15px; background-color: {'#0a2f0a' if result.score >= 75 else '#3f1f1f'}; 
                border: 3px solid {'#22c55e' if result.score >= 75 else '#ef4444'}; text-align: center;">
        <h1 style="margin: 0; color: {'#22c55e' if result.score >= 75 else '#ef4444'};">{result.score} / 100</h1>
        <h2 style="margin: 10px 0;">{result.level}</h2>
        <h3 style="margin: 10px 0; color: {'#22c55e' if result.score >= 75 else '#ef4444'};">{result.deployment}</h3>
        <p><strong>Confidence:</strong> {result.confidence}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Radar Chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(result.breakdown.values()) + [list(result.breakdown.values())[0]],
        theta=list(result.breakdown.keys()) + [list(result.breakdown.keys())[0]],
        fill='toself',
        line=dict(color='#22c55e')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Trust Metrics Radar Chart",
        height=420,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Detailed Breakdown")
    df = pd.DataFrame({
        "Metric": result.breakdown.keys(),
        "Score": result.breakdown.values(),
        "Weighted Contribution": [round(v * engine.weights[k], 1) for k, v in result.breakdown.items()]
    })
    st.dataframe(df.style.background_gradient(cmap='RdYlGn'), use_container_width=True, hide_index=True)

# Recommendations
if result.recommendations:
    st.subheader("🛠 Actionable Recommendations")
    for rec in result.recommendations:
        st.warning(f"• {rec}")
else:
    st.success("🎉 Excellent! No major issues detected. Ready for deployment.")

# History
st.divider()
st.subheader("📜 Assessment History")
if engine.history:
    history_df = pd.DataFrame([{
        "Timestamp": r.timestamp,
        "Score": r.score,
        "Level": r.level,
        "Decision": r.deployment
    } for r in engine.history])
    st.dataframe(history_df, use_container_width=True)

    if st.button("Export Full History as JSON"):
        history_json = json.dumps([vars(r) for r in engine.history], default=str, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=history_json,
            file_name=f"ai_trust_history_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

st.caption("AI Trust Copilot • Built for speed & clarity")
