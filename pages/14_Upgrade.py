import streamlit as st

st.set_page_config(page_title="Upgrade", page_icon="💎", layout="wide")

st.title("Upgrade to Pro")
st.write("Unlock premium AI trust, audit, and export features.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Free")
    st.write("Basic AI trust scan")
    st.write("Simple risk score")
    st.write("No export")

with col2:
    st.subheader("Pro")
    st.write("Advanced risk analysis")
    st.write("PDF/CSV report export")
    st.write("Audit trail access")
    st.write("Priority support")
    st.link_button("Upgrade to Pro", "https://buy.stripe.com/YOUR_STRIPE_LINK")

with col3:
    st.subheader("Enterprise")
    st.write("Team dashboard")
    st.write("Custom policies")
    st.write("Webhook integration")
    st.write("Dedicated support")

st.divider()

st.info("Secure payments are handled by Stripe Checkout or a Stripe Payment Link.")
