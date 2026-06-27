import streamlit as st

def deployment_card(result):

    if result.color == "green":
        st.success("✅ APPROVED")

    elif result.color == "orange":
        st.warning(result.status)

    else:
        st.error(result.status)

    c1, c2, c3 = st.columns(3)

    c1.metric("Confidence", f"{result.confidence}%")

    c2.metric("Risk", result.risk_level)

    c3.metric("Decision", result.status)

    st.divider()

    st.subheader("Why?")

    for reason in result.reasons:
        st.success(reason)

    if result.required_actions:

        st.subheader("Required Actions")

        for action in result.required_actions:
            st.warning(action)

    if result.blockers:

        st.subheader("Deployment Blockers")

        for blocker in result.blockers:
            st.error(blocker)

    st.divider()

    st.text(result.executive_summary)
