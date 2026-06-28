from __future__ import annotations
import time
import uuid
from datetime import datetime
import streamlit as st

# ==========================================================
# INITIALIZATION
# ==========================================================
def init_guardian():
    defaults = {
        "guardian_messages": [],
        "guardian_agent": "Auto",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ==========================================================
# STYLING
# ==========================================================
def inject_css():
    st.markdown("""
    <style>
    .chat-title{font-size:36px;font-weight:700;color:white;margin-bottom:5px;}
    .chat-sub{color:#A9B2C3;margin-bottom:20px;}
    .agent-pill{display:inline-block;padding:6px 14px;background:#2563EB;color:white;border-radius:20px;font-size:13px;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================
def hero():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown("""
        <div class='chat-title'>🛡 GuardianGPT</div>
        <div class='chat-sub'>Enterprise Responsible AI Governance Copilot</div>
        """, unsafe_allow_html=True)
    with c2:
        st.success("● Online")

# ==========================================================
# DASHBOARD
# ==========================================================
def dashboard():
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Models", "12", "+1")
    with c2: st.metric("Compliance", "94%", "+2%")
    with c3: st.metric("Risk", "Low")
    with c4: st.metric("Alerts", "3")

# ==========================================================
# SIDEBAR
# ==========================================================
def sidebar():
    st.sidebar.title("🛡 GuardianGPT")
    st.sidebar.selectbox(
        "Active Agent",
        ["Auto", "Compliance", "Risk", "Fairness", "Privacy", "Explainability", "Monitoring", "Reports"],
        key="guardian_agent"
    )
    st.sidebar.divider()
    st.sidebar.markdown("### Suggested Questions")
    
    prompts = [
        "Audit my model", "Generate Model Card", "Generate AI Nutrition Label",
        "Explain bias score", "Explain SHAP values", "Create compliance report",
        "Check EU AI Act", "Find risks", "Assess privacy risks", "Generate executive summary"
    ]
    for p in prompts:
        if st.sidebar.button(p, use_container_width=True):
            st.session_state.guardian_messages.append({
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": p,
                "time": datetime.now(),
            })
            st.rerun()

# ==========================================================
# MESSAGE HELPERS
# ==========================================================
def add_ai_message(text, agent="Guardian"):
    st.session_state.guardian_messages.append({
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "agent": agent,
        "content": text,
        "time": datetime.now(),
    })

# ==========================================================
# STREAMING EFFECT
# ==========================================================
def stream_response(text):
    placeholder = st.empty()
    output = ""
    for word in text.split():
        output += word + " "
        placeholder.markdown(output + "▌")
        time.sleep(0.018)
    placeholder.markdown(text)

# ==========================================================
# MAIN ROUTER - RICH ANSWERS FOR EVERY AGENT
# ==========================================================
def route(question: str):
    q = question.lower()
    agent = st.session_state.guardian_agent

    if agent == "Auto":
        if any(word in q for word in ["risk", "danger", "hazard"]):
            agent = "Risk"
        elif any(word in q for word in ["bias", "fairness"]):
            agent = "Fairness"
        elif any(word in q for word in ["privacy", "gdpr", "pii"]):
            agent = "Privacy"
        elif "model card" in q or "compliance" in q or "eu ai" in q:
            agent = "Compliance"
        elif any(word in q for word in ["explain", "shap", "lime"]):
            agent = "Explainability"
        elif "monitor" in q or "drift" in q:
            agent = "Monitoring"
        elif "report" in q or "summary" in q:
            agent = "Reports"

    # === RESPONSES ===
    if agent == "Risk":
        return agent, """### 🛡️ Risk Assessment
**Overall Risk**: **LOW**

**Key Findings**:
- No critical risks detected
- Moderate data drift observed
- Adversarial robustness: Good

**Recommendations**:
- Enable real-time monitoring
- Schedule quarterly audits
- Add input validation"""

    elif agent == "Fairness":
        return agent, """### ⚖️ Fairness Analysis
**Demographic Parity**: PASS  
**Equal Opportunity**: PASS  
**Equalized Odds**: PASS  

**Bias Score**: **0.07** (Very Low)  
**Status**: **LOW RISK**

Protected attributes (Gender, Race, Age) are properly handled."""

    elif agent == "Privacy":
        return agent, """### 🔒 Privacy Assessment
**Privacy Risk**: Medium

**Issues**:
- Training data may contain PII
- No differential privacy applied

**Recommendations**:
- Implement data anonymization
- Add consent tracking
- Use federated learning where possible"""

    elif agent == "Compliance":
        return agent, """### 📋 Compliance Status
**EU AI Act**: Compliant  
**ISO 42001**: 91% Compliant  

**Model Card Status**: Ready for generation"""

    elif agent == "Explainability":
        return agent, """### 🔍 Explainability Report
**Most Important Features**: transaction_amount, velocity, location_risk

**SHAP Analysis** available for individual predictions."""

    elif agent == "Monitoring":
        return agent, """### 📈 Monitoring Dashboard
**Status**: Healthy  
**Data Drift**: Warning in 1 feature  
**Prediction Latency**: 42ms"""

    elif agent == "Reports":
        return agent, """### 📊 Executive Summary
All high-risk models are compliant.  
Overall Governance Maturity: **Level 3**"""

    else:
        return "Guardian", f"""Understood: **{question}**

I can help you with **Responsible AI** topics:
- Risk Assessment
- Fairness & Bias
- Privacy & GDPR
- Model Cards & Compliance
- Explainability (SHAP)
- Monitoring & Reports

What would you like to explore?"""

# ==========================================================
# CHAT WINDOW
# ==========================================================
def chat_window():
    for msg in st.session_state.guardian_messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.caption(f"**{msg.get('agent', 'Guardian')}**")
                st.markdown(msg["content"])

# ==========================================================
# MAIN
# ==========================================================
def main():
    st.set_page_config(page_title="GuardianGPT", layout="wide")
    init_guardian()
    inject_css()

    sidebar()
    hero()
    dashboard()
    chat_window()

    prompt = st.chat_input("Ask anything about Responsible AI Governance...")
    
    if prompt:
        # Add user message
        st.session_state.guardian_messages.append({
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": prompt,
            "time": datetime.now(),
        })
        st.rerun()

    # Show AI response
    if st.session_state.guardian_messages and st.session_state.guardian_messages[-1]["role"] == "user":
        last_q = st.session_state.guardian_messages[-1]["content"]
        agent, answer = route(last_q)
        
        with st.chat_message("assistant"):
            st.caption(f"**{agent}**")
            stream_response(answer)
        
        add_ai_message(answer, agent)

if __name__ == "__main__":
    main()
