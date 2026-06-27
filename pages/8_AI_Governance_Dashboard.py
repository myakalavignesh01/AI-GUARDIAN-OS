import io
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Governance Dashboard",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ AI Governance Dashboard")
st.caption("Enterprise Responsible AI Governance Overview")

st.divider()

# ==========================================================
# SESSION VALIDATION
# ==========================================================

if "dataset" not in st.session_state:
    st.error("❌ Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"]

# ==========================================================
# LOAD SESSION SCORES
# ==========================================================

fairness = float(st.session_state.get("fairness_score", 0))
privacy = float(st.session_state.get("privacy_score", 0))
bias = float(st.session_state.get("bias_score", 0))
security = float(st.session_state.get("security_score", 0))
robustness = float(st.session_state.get("robustness_score", 0))
explainability = float(st.session_state.get("explainability_score", 0))
compliance = float(st.session_state.get("compliance_score", 0))
accuracy = float(st.session_state.get("model_accuracy", 0))

project_name = st.session_state.get(
    "project_name",
    "Current Project"
)

top_feature = st.session_state.get(
    "top_feature",
    "Not Available"
)

# ==========================================================
# GOVERNANCE SCORE
# ==========================================================

scores = [
    fairness,
    privacy,
    bias,
    security,
    robustness,
    explainability,
    compliance,
]

overall = round(sum(scores) / len(scores), 2)

st.session_state["governance_score"] = overall

# ==========================================================
# ORGANIZATION OVERVIEW
# ==========================================================

st.header("Organization Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Project",
    project_name
)

c2.metric(
    "Dataset Rows",
    len(df)
)

c3.metric(
    "Dataset Columns",
    len(df.columns)
)

c4.metric(
    "Governance Score",
    f"{overall}%"
)

st.progress(overall / 100)

st.divider()

# ==========================================================
# RESPONSIBLE AI METRICS
# ==========================================================

st.header("Responsible AI Metrics")

metric_df = pd.DataFrame({

    "Metric": [

        "Fairness",

        "Privacy",

        "Bias",

        "Security",

        "Robustness",

        "Explainability",

        "Compliance"

    ],

    "Score": [

        fairness,

        privacy,

        bias,

        security,

        robustness,

        explainability,

        compliance

    ]

})

st.dataframe(
    metric_df,
    use_container_width=True,
    hide_index=True
)

fig = px.bar(
    metric_df,
    x="Metric",
    y="Score",
    color="Metric",
    text="Score",
    title="Responsible AI Metrics"
)

fig.update_layout(
    height=450,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# COMPLIANCE OVERVIEW
# ==========================================================

st.header("Compliance Overview")

left, right = st.columns(2)

with left:

    pie = px.pie(
        metric_df,
        names="Metric",
        values="Score",
        title="Governance Distribution"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

with right:

    st.metric(
        "Model Accuracy",
        f"{accuracy:.2f}%"
    )

    st.metric(
        "Top Feature",
        top_feature
    )

    st.metric(
        "Compliance",
        f"{compliance:.2f}%"
    )

st.divider()
# ==========================================================
# EXECUTIVE SCORECARD
# ==========================================================

st.header("Executive Scorecard")

scorecard = pd.DataFrame({

    "Metric":[

        "Fairness",

        "Privacy",

        "Bias",

        "Security",

        "Robustness",

        "Explainability",

        "Compliance",

        "Model Accuracy",

        "Overall Governance"

    ],

    "Score":[

        fairness,

        privacy,

        bias,

        security,

        robustness,

        explainability,

        compliance,

        accuracy,

        overall

    ]

})

st.dataframe(

    scorecard,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# GOVERNANCE STATUS
# ==========================================================

st.header("Governance Status")

if overall >= 90:

    status = "Excellent"

    risk = "Low"

    st.success("🟢 Enterprise AI Governance is Excellent")

elif overall >= 75:

    status = "Good"

    risk = "Medium"

    st.warning("🟡 Governance is Good")

else:

    status = "Needs Improvement"

    risk = "High"

    st.error("🔴 Governance Requires Immediate Attention")

st.session_state["governance_status"] = status

g1, g2, g3 = st.columns(3)

g1.metric(

    "Governance Score",

    f"{overall}%"

)

g2.metric(

    "Risk Level",

    risk

)

g3.metric(

    "Status",

    status

)

st.divider()

# ==========================================================
# GOVERNANCE RECOMMENDATIONS
# ==========================================================

st.header("Recommendations")

recommendations = []

if fairness < 80:

    recommendations.append(
        "Improve fairness by balancing the training dataset."
    )

if privacy < 80:

    recommendations.append(
        "Improve privacy using anonymization."
    )

if bias < 80:

    recommendations.append(
        "Reduce algorithmic bias."
    )

if security < 80:

    recommendations.append(
        "Improve AI security controls."
    )

if robustness < 80:

    recommendations.append(
        "Increase robustness testing."
    )

if explainability < 80:

    recommendations.append(
        "Improve explainability with SHAP/LIME."
    )

if compliance < 80:

    recommendations.append(
        "Increase compliance with Responsible AI policies."
    )

if not recommendations:

    st.success(
        "No governance issues detected."
    )

else:

    for rec in recommendations:

        st.warning(rec)

st.session_state["governance_recommendations"] = len(recommendations)

st.divider()

# ==========================================================
# AI GOVERNANCE SUMMARY
# ==========================================================

st.header("Governance Summary")

summary = f"""
Project : {project_name}

Overall Governance Score : {overall:.2f}%

Risk Level : {risk}

Governance Status : {status}

Dataset Rows : {len(df)}

Dataset Columns : {len(df.columns)}

Top Feature : {top_feature}

Model Accuracy : {accuracy:.2f}%
"""

st.info(summary)

st.divider()
# ==========================================================
# RISK DISTRIBUTION
# ==========================================================

st.header("Risk Distribution")

risk_df = pd.DataFrame({

    "Metric":[

        "Fairness",

        "Privacy",

        "Bias",

        "Security",

        "Robustness",

        "Explainability",

        "Compliance"

    ],

    "Score":[

        fairness,

        privacy,

        bias,

        security,

        robustness,

        explainability,

        compliance

    ]

})

risk_df["Risk Level"] = risk_df["Score"].apply(

    lambda x:
    "Low" if x >= 90 else
    "Medium" if x >= 75 else
    "High"

)

pie = px.pie(

    risk_df,

    names="Risk Level",

    title="AI Governance Risk Distribution"

)

st.plotly_chart(

    pie,

    use_container_width=True

)

st.divider()

# ==========================================================
# SCORE COMPARISON
# ==========================================================

st.header("Score Comparison")

fig = px.line(

    metric_df,

    x="Metric",

    y="Score",

    markers=True,

    title="Responsible AI Score Trend"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.header("Project Information")

left, right = st.columns(2)

with left:

    st.metric(

        "Project",

        project_name

    )

    st.metric(

        "Rows",

        len(df)

    )

    st.metric(

        "Columns",

        len(df.columns)

    )

with right:

    st.metric(

        "Top Feature",

        top_feature

    )

    st.metric(

        "Accuracy",

        f"{accuracy:.2f}%"

    )

    st.metric(

        "Governance",

        f"{overall:.2f}%"

    )

st.divider()

# ==========================================================
# EXPORT GOVERNANCE REPORT
# ==========================================================

st.header("Export Dashboard")

buffer = io.BytesIO()

with pd.ExcelWriter(

    buffer,

    engine="openpyxl"

) as writer:

    metric_df.to_excel(

        writer,

        sheet_name="Metrics",

        index=False

    )

    scorecard.to_excel(

        writer,

        sheet_name="Executive Scorecard",

        index=False

    )

    risk_df.to_excel(

        writer,

        sheet_name="Risk Distribution",

        index=False

    )

st.download_button(

    "⬇ Download Governance Dashboard",

    buffer.getvalue(),

    "AI_Governance_Dashboard.xlsx",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)

st.divider()

# ==========================================================
# FINAL STATUS
# ==========================================================

st.header("Executive Status")

if overall >= 90:

    st.success(
        "🟢 Enterprise AI Governance Approved"
    )

elif overall >= 75:

    st.warning(
        "🟡 Enterprise AI Governance Requires Minor Improvements"
    )

else:

    st.error(
        "🔴 Enterprise AI Governance Failed"
    )

st.success("""

AI Governance Dashboard Loaded Successfully.

✓ Responsible AI Monitoring

✓ Fairness Tracking

✓ Privacy Assessment

✓ Explainability Monitoring

✓ Compliance Tracking

✓ Governance Reporting

✓ Executive Analytics

""")

st.session_state["governance_dashboard"] = True
st.session_state["overall_governance"] = overall
st.session_state["executive_status"] = status

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "AI Guardian OS • Enterprise Responsible AI Governance Dashboard"
)
