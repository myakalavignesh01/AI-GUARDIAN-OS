import streamlit as st
import os

st.set_page_config(
    page_title="AI Guardian OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_file = "assets/styles.css"
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ AI Guardian OS")
    st.caption("Responsible AI Platform")
    st.divider()
    st.success("System Status: Online")
    st.metric("Compliance", "94%")
    st.metric("Models", "12")
    st.metric("Projects", "8")
    st.divider()
    st.info("Use the pages below to navigate the full Responsible AI workflow.")

    st.page_link("streamlit_app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Risk_Analyzer.py", label="Risk Analyzer", icon="🔎")
    st.page_link("pages/2_Demo_Scenarios.py", label="Demo Scenarios", icon="🎬")
    st.page_link("pages/3_Audit_Report.py", label="Audit Report", icon="📄")
    st.page_link("pages/4_Settings.py", label="Settings", icon="⚙️")

col1, col2 = st.columns([4, 1])

with col1:
    st.title("🛡️ AI Guardian OS")
    st.write("Enterprise Responsible AI Governance Platform")
    st.write("Analyze • Explain • Monitor • Govern")

with col2:
    st.metric("Risk Score", "LOW")

st.divider()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Compliance", "94%", "+3%")
c2.metric("Fairness", "91%", "+2%")
c3.metric("Privacy", "93%", "+1%")
c4.metric("Explainability", "95%", "+5%")

st.divider()

st.header("Welcome")
st.write(
    """
AI Guardian OS helps organizations build Responsible AI systems by providing:
- Dataset Validation
- Bias Detection
- Privacy Scanning
- Explainability
- Compliance Reports
- AI Governance
- Live Monitoring
"""
)

st.info("Open the sidebar pages to begin your Responsible AI workflow.")

try:
    from components.guardian_chatbot import guardian_chat
    guardian_chat()
except Exception:
    st.caption("Chat assistant unavailable right now.")
