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
# STREAMING
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
# ROUTER WITH RICH ANSWERS
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
        elif any(word in q for word in ["model card", "compliance", "eu ai", "iso"]):
            agent = "Compliance"
        elif any(word in q for word in ["explain", "shap", "lime"]):
            agent = "Explainability"
        elif any(word in q for word in ["monitor", "drift"]):
            agent = "Monitoring"
        elif any(word in q for word in ["report", "summary"]):
            agent = "Reports"

    # === DETAILED RESPONSES ===
    if agent == "Risk":
        return agent, """### 🛡️ Risk Assessment\n**Overall Risk**: **LOW**\n\n**Key Findings**:\n- No critical risks detected\n- Moderate data drift observed\n\n**Recommendations**:\n- Enable real-time monitoring\n- Schedule quarterly audits"""
    
    elif agent == "Fairness":
        return agent, """### ⚖️ Fairness Analysis\n**Demographic Parity**: PASS  \n**Equal Opportunity**: PASS  \n**Bias Score**: **0.07** (Very Low)\n\n**Status**: LOW RISK"""
    
    elif agent == "Privacy":
        return agent, """### 🔒 Privacy Assessment\n**Privacy Risk**: Medium\n\n**Recommendations**:\n- Implement data anonymization\n- Add consent tracking"""
    
    elif agent == "Compliance":
        return agent, """### 📋 Compliance Status\n**EU AI Act**: Compliant  \n**ISO 42001**: 91% Compliant\n\n**Model Card**: Ready"""
    
    elif agent == "Explainability":
        return agent, """### 🔍 Explainability Report\n**SHAP Analysis** available.\nTop features: transaction_amount, velocity"""
    
    elif agent == "Monitoring":
        return agent, """### 📈 Monitoring\n**Status**: Healthy\n**Data Drift**: Warning in 1 feature"""
    
    elif agent == "Reports":
        return agent, """### 📊 Executive Summary\nAll high-risk models are compliant."""
    
    else:
        return "Guardian", f"Understood: **{question}**\n\nHow can I help you with Responsible AI today?"

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
# MAIN FUNCTION (Export this)
# ==========================================================
def guardian_chat():
    init_guardian()
    inject_css()
    
    sidebar()
    hero()
    dashboard()
    chat_window()

    prompt = st.chat_input("Ask GuardianGPT anything about Responsible AI...")
    
    if prompt:
        st.session_state.guardian_messages.append({
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": prompt,
            "time": datetime.now(),
        })
        st.rerun()

    # AI Response
    if st.session_state.guardian_messages and st.session_state.guardian_messages[-1]["role"] == "user":
        last_q = st.session_state.guardian_messages[-1]["content"]
        agent, answer = route(last_q)
        
        with st.chat_message("assistant"):
            st.caption(f"**{agent}**")
            stream_response(answer)
        
        st.session_state.guardian_messages.append({
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "agent": agent,
            "content": answer,
            "time": datetime.now(),
        })
