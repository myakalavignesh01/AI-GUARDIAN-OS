import streamlit as st  
from datetime import datetime  
import uuid  

st.set_page_config(page_title="AI Trust Certificate", page_icon="🛡️", layout="wide")  

st.title("🛡️ AI Guardian OS")  
st.subheader("AI Trust Score & Certificate")  

# Get scores from previous pages if available  
fairness = st.session_state.get("fairness_score", 90)  
privacy = st.session_state.get("privacy_score", 95)  
explainability = st.session_state.get("explainability_score", 92)  
compliance = st.session_state.get("compliance_score", 91)  
quality = st.session_state.get("data_quality_score", 89)  

# Trust Score  
trust_score = round(  
    fairness * 0.25 +  
    privacy * 0.20 +  
    explainability * 0.20 +  
    compliance * 0.20 +  
    quality * 0.15  
)  

if trust_score >= 80:  
    status = "🟢 APPROVED FOR DEPLOYMENT"  
elif trust_score >= 60:  
    status = "🟡 REVIEW REQUIRED"  
else:  
    status = "🔴 REJECTED"  

st.markdown("---")  

c1, c2, c3 = st.columns(3)  

c1.metric("🛡️ AI Trust Score", f"{trust_score}/100")  
c2.metric("Fairness", f"{fairness}%")  
c3.metric("Privacy", f"{privacy}%")  

st.progress(trust_score / 100)  

st.success(status)  

st.markdown("## Score Breakdown")  

st.table({  
    "Category": [  
        "Fairness",  
        "Privacy",  
        "Explainability",  
        "Compliance",  
        "Data Quality"  
    ],  
    "Score": [  
        fairness,  
        privacy,  
        explainability,  
        compliance,  
        quality  
    ]  
})  

st.markdown("---")  

certificate_id = "AIG-" + str(uuid.uuid4())[:8].upper()  

st.markdown("## 📜 AI Trust Certificate")  

# Real certificate using HTML/CSS  
cert_html = f"""  
<div style="  
    background: linear-gradient(135deg, #fdf8f0, #f5ead0);  
    border: 8px double #b8860b;  
    border-radius: 8px;  
    padding: 35px 40px;  
    margin: 15px 0;  
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);  
    position: relative;  
    font-family: 'Georgia', 'Times New Roman', serif;  
">  
    <!-- Inner border -->  
    <div style="  
        position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px;  
        border: 1px solid rgba(184,134,11,0.25);  
        pointer-events: none;  
    "></div>  

    <!-- Watermark -->  
    <div style="  
        position: absolute; top: 50%; left: 50%;  
        transform: translate(-50%, -50%) rotate(-25deg);  
        font-size: 120px; font-weight: bold;  
        color: rgba(184,134,11,0.06);  
        white-space: nowrap; pointer-events: none;  
    ">AI GUARDIAN</div>  

    <!-- Seal & Org -->  
    <div style="text-align: center; position: relative; z-index: 1;">  
        <div style="font-size: 48px;">🛡️</div>  
        <div style="  
            font-size: 24px; font-weight: bold; color: #2c1810;  
            letter-spacing: 3px; text-transform: uppercase;  
            font-family: Arial, sans-serif;  
        ">AI Guardian OS</div>  
        <div style="  
            font-size: 12px; color: #7a6b52; letter-spacing: 4px;  
            text-transform: uppercase; margin-top: 2px;  
        ">Responsible AI Assessment System</div>  
    </div>  

    <!-- Gold divider -->  
    <div style="  
        width: 60%; height: 2px; margin: 15px auto;  
        background: linear-gradient(to right, transparent, #b8860b, transparent);  
    "></div>  

    <!-- Title -->  
    <div style="text-align: center; position: relative; z-index: 1;">  
        <h2 style="  
            font-size: 30px; color
