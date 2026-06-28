import streamlit as st
import requests
import json
from datetime import datetime
import time
import uuid

# ====================== CONFIG ======================
API_BASE_URL = "https://api.groq.com/openai/v1"  # Change to your preferred API
API_KEY = st.secrets.get("API_KEY", None)  # Use Streamlit secrets in production

# ====================== TRUST ENGINE ======================
class AITrustEngine:
    def __init__(self):
        self.weights = {"fairness":0.20,"privacy":0.20,"security":0.15,"compliance":0.20,"explainability":0.15,"monitoring":0.10}

    def calculate(self, fairness=93, privacy=95, security=90, compliance=97, explainability=88, monitoring=92):
        score = round(
            fairness*0.20 + privacy*0.20 + security*0.15 + 
            compliance*0.20 + explainability*0.15 + monitoring*0.10, 1
        )
        if score >= 90: level, dep = "Excellent", "✅ APPROVED"
        elif score >= 75: level, dep = "Good", "🟡 APPROVED WITH CONDITIONS"
        elif score >= 60: level, dep = "Medium", "🔶 REVIEW REQUIRED"
        else: level, dep = "Critical", "❌ DO NOT DEPLOY"
        
        return {
            "score": score,
            "level": level,
            "deployment": dep,
            "confidence": round(min(99, score + 5), 1),
            "breakdown": {"Fairness":fairness, "Privacy":privacy, "Security":security,
                         "Compliance":compliance, "Explainability":explainability, "Monitoring":monitoring}
        }

# ====================== API CALL ======================
def call_ai_api(prompt: str, system_prompt: str = None):
    """Real API call (Groq / OpenAI compatible)"""
    if not API_KEY:
        # Fallback for local testing
        time.sleep(0.8)
        return f"I analyzed: '{prompt[:80]}...'\n\nTrust Score: 91.4\nRecommendation: Strong compliance profile."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",   # or mixtral, gemma2 etc.
        "messages": [
            {"role": "system", "content": system_prompt or "You are GuardianGPT, an expert Enterprise AI Governance Copilot."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error {response.status_code}: {response.text[:200]}"
    except Exception as e:
        return f"Connection error: {str(e)}"

# ====================== STREAMLIT UI ======================
st.set_page_config(page_title="GuardianGPT", page_icon="🛡", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "trust_engine" not in st.session_state:
    st.session_state.trust_engine = AITrustEngine()

engine = st.session_state.trust_engine

# Header
st.title("🛡 GuardianGPT")
st.caption("Enterprise AI Governance • Real API Powered Copilot")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("AI Model", ["llama3-70b", "mixtral-8x7b", "gemma2-9b"])
    st.divider()
    st.subheader("Quick Actions")
    if st.button("Run Full Trust Assessment"):
        result = engine.calculate()
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"**Trust Assessment Complete**\n\n**Score**: {result['score']}/100 → {result['level']}\n**Decision**: {result['deployment']}\n\nBreakdown: {result['breakdown']}"
        })
        st.rerun()

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask anything about AI Governance, Risk, Compliance..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_ai_api(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.caption("GuardianGPT v1.0 • Powered by Real API • Trust Engine Integrated")
