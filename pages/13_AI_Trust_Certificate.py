import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="AI Trust Certificate", 
    page_icon="🛡️", 
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main-title { color: #ffffff; font-size: 32px; font-weight: bold; }
    .sub-title { color: #9e9e9e; font-size: 16px; }
    .cert-container { 
        background: linear-gradient(135deg, #1a1d27, #222736); 
        border: 1px solid #2a2d3a; 
        border-radius: 16px; 
        padding: 35px; 
        margin: 20px 0; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.3); 
    }
    .cert-header { 
        display: flex; 
        align-items: center; 
        gap: 12px; 
        border-bottom: 1px solid #2a2d3a; 
        padding-bottom: 15px; 
        margin-bottom: 20px; 
    }
    .cert-badge { 
        background: #2a6b3c; 
        color: white; 
        padding: 4px 14px; 
        border-radius: 20px; 
        font-size: 12px; 
        font-weight: bold; 
    }
    .metric-box { 
        background: #1e2130; 
        border: 1px solid #2a2d3a; 
        border-radius: 10px; 
        padding: 15px; 
        text-align: center; 
    }
    .metric-value { 
        color: white; 
        font-size: 28px; 
        font-weight: bold; 
    }
    .metric-label { 
        color: #9e9e9e; 
        font-size: 12px; 
        margin-top: 5px; 
    }
    .score-row { 
        display: flex; 
        justify-content: space-between; 
        padding: 10px 0; 
        border-bottom: 1px solid #1e2130; 
    }
    .score-label { color: #b0b0b0; }
    .score-value { color: #4caf50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Titles
st.markdown("""
    <h1 class="main-title">🛡️ AI Guardian OS</h1>
""", unsafe_allow_html=True)

st.markdown("""
    <h2 class="sub-title">AI Trust Score & Certificate</h2>
""", unsafe_allow_html=True)

# Get scores from session state
fairness = st.session_state.get("fairness_score", 90)
privacy = st.session_state.get("privacy_score", 95)
explainability = st.session_state.get("explainability_score", 92)
compliance = st.session_state.get("compliance_score", 91)
quality = st.session_state.get("data_quality_score", 89)

# Calculate trust score
trust_score = round(
    fairness * 0.25 + 
    privacy * 0.20 + 
    explainability * 0.20 + 
    compliance * 0.20 + 
    quality * 0.15
)

if trust_score >= 80:
    status = "DEPLOYMENT APPROVED"
    status_color = "#4caf50"
elif trust_score >= 60:
    status = "REVIEW REQUIRED"
    status_color = "#ff9800"
else:
    status = "REJECTED"
    status_color = "#f44336"

st.markdown("---")

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{trust_score}</div>
            <div class="metric-label">AI Trust Score / 100</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{fairness}%</div>
            <div class="metric-label">Fairness</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{privacy}%</div>
            <div class="metric-label">Privacy</div>
        </div>
    """, unsafe_allow_html=True)
