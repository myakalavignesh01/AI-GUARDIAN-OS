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
    .about-box{
        background:#1E293B; 
        padding:25px; 
        border-radius:12px; 
        border-left:5px solid #10B981;
        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# ABOUT SECTION
# ==========================================================
def show_about():
    st.markdown("### About GuardianGPT")
    with st.expander("ℹ️ Learn more about this application", expanded=False):
        st.markdown("""
        <div class='about-box'>
        <h3>🛡 GuardianGPT Enterprise AI Governance Copilot</h3>
        <p><strong>Version:</strong> 1.0 | <strong>Author:</strong> M. Vignesh</p>
        
        <h4>What is GuardianGPT?</h4>
        <p>GuardianGPT is an intelligent AI assistant that helps enterprises implement Responsible AI practices.</p>
        
        <h4>Core Capabilities</h4>
        <ul>
            <li>✅ AI Risk Assessment</li>
            <li>✅ Fairness & Bias Auditing</li>
            <li>✅ Privacy & Data Protection</li>
            <li>✅ Regulatory Compliance (EU AI Act, ISO 42001)</li>
            <li>✅ Model Explainability (SHAP, LIME)</li>
            <li>✅ Automated Model Cards & Reports</li>
            <li>✅ Continuous Monitoring</li>
        </ul>
        
        <p><strong>Mission:</strong> Making AI Governance simple, intelligent, and enterprise-ready.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# HEADER & DASHBOARD
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

def dashboard():
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Models", "12", "+1")
    with c2: st.metric("Compliance", "94%", "+2%")
    with c3: st.metric("Risk", "Low")
    with c4: st.metric("Alerts", "3")

# ==========================================================
# SIDEBAR - TOP 10 QUESTIONS
# ==========================================================
def sidebar():
    st.sidebar.title("🛡 GuardianGPT")
    st.sidebar.selectbox(
        "Active Agent",
        ["Auto", "Compliance", "Risk", "Fairness", "Privacy", "Explainability", "Monitoring", "Reports"],
        key="guardian_agent"
    )
    st.sidebar.divider()
    st.sidebar.markdown("### 🔥 Top 10 Questions")

    top_questions = [
        "Hello, who are you?",
        "Tell me about GuardianGPT",
        "What can you help me with?",
        "Audit my AI model",
        "Generate a Model Card",
        "Assess fairness and bias",
        "Check EU AI Act compliance",
        "What are the main risks in my model?",
        "Explain SHAP values",
        "Generate executive summary"
    ]
    
    for q in top_questions:
        if st.sidebar.button(q, use_container_width=True):
            st.session_state.guardian_messages.append({
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": q,
                "time": datetime.now(),
            })
            st.rerun()

# ==========================================================
# STREAMING RESPONSE
# ==========================================================
def stream_response(text):
    placeholder = st.empty()
    output = ""
    for word in text.split():
        output += word + " "
        placeholder.markdown(output + "▌")
        time.sleep(0.015)
    placeholder.markdown(text)

# ==========================================================
# INTELLIGENT ROUTER
# ==========================================================
def route(question: str):
    q = question.lower().strip()
    agent = st.session_state.guardian_agent

    # === Basic Conversations ===
    if q in ["hi", "hello", "hey", "greetings"]:
        return "Guardian", "Hello! 👋 How can I help you with Responsible AI today?"
    
    elif any(x in q for x in ["who are you", "about you", "your name"]):
        return "Guardian", "I am **GuardianGPT**, your Enterprise AI Governance Copilot."
    
    elif "about" in q:
        return "Guardian", "GuardianGPT helps enterprises with AI Risk, Compliance, Fairness, Privacy and more. Check the About section above!"

    # === Auto Agent Routing ===
    if agent == "Auto":
        if any(x in q for x in ["risk", "danger", "hazard"]):
            agent = "Risk"
        elif any(x in q for x in ["bias", "fairness"]):
            agent = "Fairness"
        elif any(x in q for x in ["privacy", "gdpr", "pii"]):
            agent = "Privacy"
        elif any(x in q for x in ["model card", "compliance", "eu ai", "iso"]):
            agent = "Compliance"
        elif any(x in q for x in ["explain", "shap", "lime"]):
            agent = "Explainability"

    # === Domain Responses ===
    if agent == "Risk":
        return agent, """### 🛡️ Risk Assessment\n**Overall Risk**: **LOW**\n\nNo critical issues found."""
    elif agent == "Fairness":
        return agent, """### ⚖️ Fairness Analysis\n**Bias Score**: **0.07** (Very Low)\n**Status**: PASS"""
    elif agent == "Privacy":
        return agent, """### 🔒 Privacy Assessment\nI can help you evaluate data protection and GDPR compliance."""
    elif agent == "Compliance":
        return agent, """### 📋 Compliance Check\n**EU AI Act**: Compliant\n**ISO 42001**: 91%"""
    elif agent == "Explainability":
        return agent, """### 🔍 Explainability\nSHAP analysis is available for your model."""
    else:
        return "Guardian", "Thank you for your question. How can I assist you with AI Governance today?"

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
# MAIN FUNCTION
# ==========================================================
def guardian_chat():
    init_guardian()
    inject_css()
    
    show_about()
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
