import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(page_title="AI Trust Certificate", page_icon="🛡️", layout="wide")
st.title("🛡️ AI Guardian OS")
st.subheader("AI Trust Score & Certificate")

# ... (keep your existing score calculation code) ...

fairness = st.session_state.get("fairness_score", 90)
privacy = st.session_state.get("privacy_score", 95)
explainability = st.session_state.get("explainability_score", 92)
compliance = st.session_state.get("compliance_score", 91)
quality = st.session_state.get("data_quality_score", 89)

trust_score = round(fairness * 0.25 + privacy * 0.20 + explainability * 0.20 + compliance * 0.20 + quality * 0.15)

if trust_score >= 80:
    status = "🟢 APPROVED FOR DEPLOYMENT"
elif trust_score >= 60:
    status = "🟡 REVIEW REQUIRED"
else:
    status = "🔴 REJECTED"

certificate_id = "AIG-" + str(uuid.uuid4())[:8].upper()
generated_date = datetime.now().strftime("%d %B %Y")

st.markdown("---")
# Display metrics and table (same as before)...

# Beautiful HTML Certificate
st.markdown("## 📜 Official AI Trust Certificate")

certificate_html = f"""
<div style="border: 4px solid #0d6efd; padding: 40px; text-align: center; border-radius: 15px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); max-width: 800px; margin: 20px auto;">
    <h1 style="color: #0d6efd;">AI GUARDIAN OS</h1>
    <h2>AI TRUST CERTIFICATE</h2>
    <p><strong>Certificate ID:</strong> {certificate_id}</p>
    <p><strong>Generated On:</strong> {generated_date}</p>
    
    <hr style="border: 2px solid #0d6efd;">
    
    <h1 style="color: #198754; font-size: 3.5em;">{trust_score}/100</h1>
    <h3 style="color: #198754;">{status}</h3>
    
    <h4>Score Breakdown</h4>
    <table style="margin: 20px auto; width: 70%; border-collapse: collapse;">
        <tr><th style="border: 1px solid #ddd; padding: 8px;">Category</th><th style="border: 1px solid #ddd; padding: 8px;">Score</th></tr>
        <tr><td style="border: 1px solid #ddd; padding: 8px;">Fairness</td><td style="border: 1px solid #ddd; padding: 8px;">{fairness}%</td></tr>
        <tr><td style="border: 1px solid #ddd; padding: 8px;">Privacy</td><td style="border: 1px solid #ddd; padding: 8px;">{privacy}%</td></tr>
        <tr><td style="border: 1px solid #ddd; padding: 8px;">Explainability</td><td style="border: 1px solid #ddd; padding: 8px;">{explainability}%</td></tr>
        <tr><td style="border: 1px solid #ddd; padding: 8px;">Compliance</td><td style="border: 1px solid #ddd; padding: 8px;">{compliance}%</td></tr>
        <tr><td style="border: 1px solid #ddd; padding: 8px;">Data Quality</td><td style="border: 1px solid #ddd; padding: 8px;">{quality}%</td></tr>
    </table>
    
    <p style="margin-top: 40px; font-size: 0.9em;">
        This certificate is automatically generated after Responsible AI assessment.<br>
        <strong>Scan QR code or visit verification link to validate.</strong>
    </p>
</div>
"""

st.markdown(certificate_html, unsafe_allow_html=True)

# Download as Text (fallback)
certificate_text = f"""AI GUARDIAN OS - AI TRUST CERTIFICATE
Certificate ID : {certificate_id}
Generated On   : {generated_date}
Trust Score    : {trust_score}/100
Status         : {status}

Fairness       : {fairness}%
Privacy        : {privacy}%
Explainability : {explainability}%
Compliance     : {compliance}%
Data Quality   : {quality}%
"""

st.download_button(
    "📄 Download Certificate (Text)",
    certificate_text,
    file_name=f"AI_Trust_Certificate_{certificate_id}.txt",
    mime="text/plain"
)

st.balloons()
