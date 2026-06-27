"""
GuardianGPT Enterprise AI Governance Copilot
Author : M. Vignesh
Version : 1.0

Main Chat UI
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime

import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

def init_guardian():
    """Initialize session state."""

    defaults = {
        "guardian_messages": [],
        "guardian_memory": [],
        "guardian_uploads": [],
        "guardian_thinking": False,
        "guardian_theme": "dark",
        "guardian_agent": "Auto",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ==========================================================
# STYLING
# ==========================================================

def inject_css():
    st.markdown(
        """
<style>

.chat-title{
font-size:34px;
font-weight:700;
color:white;
margin-bottom:5px;
}

.chat-sub{
color:#A9B2C3;
margin-bottom:20px;
}

.user-box{
background:#0F172A;
padding:14px;
border-radius:12px;
margin:8px 0;
border-left:5px solid #3B82F6;
}

.ai-box{
background:#1E293B;
padding:14px;
border-radius:12px;
margin:8px 0;
border-left:5px solid #10B981;
}

.metric-card{
background:#111827;
padding:12px;
border-radius:12px;
text-align:center;
}

.small{
font-size:13px;
color:#A0AEC0;
}

.agent-pill{
display:inline-block;
padding:6px 14px;
background:#2563EB;
color:white;
border-radius:20px;
margin-right:8px;
margin-bottom:8px;
font-size:13px;
}

</style>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# HEADER
# ==========================================================

def hero():

    c1, c2 = st.columns([4, 1])

    with c1:

        st.markdown(
            """
<div class='chat-title'>
🛡 GuardianGPT
</div>
<div class='chat-sub'>
Enterprise Responsible AI Copilot
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.success("● Online")


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard():

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Models", "12", "+1")

    with c2:
        st.metric("Compliance", "94%", "+2%")

    with c3:
        st.metric("Risk", "Low")

    with c4:
        st.metric("Alerts", "3")


# ==========================================================
# SIDEBAR
# ==========================================================

def sidebar():

    st.sidebar.title("GuardianGPT")

    st.sidebar.selectbox(
        "Active Agent",
        [
            "Auto",
            "Compliance",
            "Risk",
            "Fairness",
            "Privacy",
            "Explainability",
            "Monitoring",
            "Reports",
        ],
        key="guardian_agent",
    )

    st.sidebar.divider()

    st.sidebar.markdown("### Suggested Questions")

    prompts = [
        "Audit my model",
        "Generate Model Card",
        "Generate AI Nutrition Label",
        "Explain bias score",
        "Explain SHAP values",
        "Create compliance report",
        "Check EU AI Act",
        "Check ISO 42001",
        "Find risks",
        "Generate executive summary",
    ]

    for p in prompts:
        if st.sidebar.button(p, use_container_width=True):
            add_user_message(p)


# ==========================================================
# MESSAGE HELPERS
# ==========================================================

def add_user_message(text):

    st.session_state.guardian_messages.append(
        {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": text,
            "time": datetime.now(),
        }
    )


def add_ai_message(text, agent="Guardian"):

    st.session_state.guardian_messages.append(
        {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "agent": agent,
            "content": text,
            "time": datetime.now(),
        }
    )


# ==========================================================
# STREAMING
# ==========================================================

def stream(text):

    placeholder = st.empty()

    output = ""

    for word in text.split():

        output += word + " "

        placeholder.markdown(output)

        time.sleep(0.02)

    return output


# ==========================================================
# SIMPLE ROUTER (temporary)
# This will be replaced by ai_router.py later.
# ==========================================================

def route(question):

    q = question.lower()

    if "risk" in q:

        return (
            "Risk Agent",
            """
### Risk Assessment

Overall Risk : LOW

Critical Issues
- Missing monitoring alerts
- Model card needs updating

Recommendation
- Enable drift monitoring
- Schedule bias audit
- Review privacy controls
""",
        )

    elif "bias" in q or "fairness" in q:

        return (
            "Fairness Agent",
            """
### Fairness Analysis

Demographic Parity : PASS

Equal Opportunity : PASS

Equalized Odds : PASS

Protected Attributes

✓ Gender ignored

✓ Religion ignored

✓ Race ignored

Bias Score

0.07

Status

LOW RISK
""",
        )

    elif "model card" in q:

        return (
            "Compliance Agent",
            """
## AI Model Card

Model

Fraud Detection

Version

2.3

Accuracy

96.8%

Risk

LOW

Owner

AI Guardian OS

Deployment

Approved
""",
        )

    else:

        return (
            "Guardian",
            f"""
I understood:

> {question}

I can help you with:

• AI Governance

• Compliance

• Fairness

• Privacy

• Risk

• Explainability

• Monitoring

• Executive Reports
""",
        )


# ==========================================================
# CHAT WINDOW
# ==========================================================

def chat_window():

    for message in st.session_state.guardian_messages:

        if message["role"] == "user":

            with st.chat_message("user"):
                st.markdown(message["content"])

        else:

            with st.chat_message("assistant"):

                st.caption(message.get("agent", "Guardian"))

                st.markdown(message["content"])


# ==========================================================
# MAIN
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

        add_user_message(prompt)

        agent, answer = route(prompt)

        with st.chat_message("assistant"):

            st.caption(agent)

            stream(answer)

        add_ai_message(answer, agent)
