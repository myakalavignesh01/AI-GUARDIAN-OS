import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

from database.database import get_connection

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(

    page_title="Compliance Report",

    page_icon="📑",

    layout="wide"

)

st.title("📑 Responsible AI Compliance Report")

st.caption(

    "Generate enterprise Responsible AI compliance reports."

)

st.divider()
# -----------------------------------------------------
# Load Analysis Results
# -----------------------------------------------------

if "dataset" not in st.session_state:
    st.error("❌ Please upload a dataset first from the Upload Dataset page.")
    st.stop()

df = st.session_state["dataset"]

fairness = st.session_state.get("fairness_score", 0.0)
privacy = st.session_state.get("privacy_score", 0.0)
explainability = st.session_state.get("explainability_score", 0.0)
accuracy = st.session_state.get("model_accuracy", 0.0)

dataset = {
    "rows": len(df),
    "columns": len(df.columns),
    "filename": st.session_state.get("dataset_name", "Uploaded Dataset")
}

project_id = st.session_state.get("project_name", "Current Session")

st.success("✅ Analysis results loaded successfully.")

st.divider()

# -----------------------------------------------------
# Compliance Dashboard
# -----------------------------------------------------

st.header("Compliance Dashboard")

overall = round(
    (
        fairness +
        privacy +
        explainability +
        accuracy
    ) / 4,
    2
)

st.session_state["compliance_score"] = overall

c1, c2, c3, c4 = st.columns(4)

c1.metric("Fairness", f"{fairness:.2f}%")
c2.metric("Privacy", f"{privacy:.2f}%")
c3.metric("Explainability", f"{explainability:.2f}%")
c4.metric("Overall", f"{overall:.2f}%")

st.progress(overall / 100)

st.divider()

# -----------------------------------------------------
# Executive Summary
# -----------------------------------------------------

st.header("Executive Summary")

if overall >= 90:
    risk_level = "LOW"
elif overall >= 75:
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"

st.session_state["risk_level"] = risk_level

summary = f"""
The Responsible AI assessment has been completed successfully.

Overall Compliance Score : {overall:.2f}%

Risk Level : {risk_level}

The evaluation includes:

• Fairness Assessment
• Privacy Protection
• Model Explainability
• Model Accuracy
• Governance Readiness

This report summarizes the current Responsible AI posture
and identifies areas requiring improvement before production deployment.
"""

st.info(summary)
st.success("✅ Compliance analysis completed.")

st.divider()

# -----------------------------------------------------
# Dataset Information
# -----------------------------------------------------

st.header("Dataset Information")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Rows",
    dataset["rows"]
)

c2.metric(
    "Columns",
    dataset["columns"]
)

c3.metric(
    "Dataset",
    dataset["filename"]
)

st.divider()

# -----------------------------------------------------
# Compliance Scorecard
# -----------------------------------------------------

st.header("Compliance Scorecard")

score_df = pd.DataFrame({
    "Category": [
        "Fairness",
        "Privacy",
        "Explainability",
        "Accuracy",
        "Overall"
    ],
    "Score": [
        fairness,
        privacy,
        explainability,
        accuracy,
        overall
    ]
})

st.dataframe(
    score_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    score_df.set_index("Category")
)

st.divider()

# -----------------------------------------------------
# Compliance Checklist
# -----------------------------------------------------

st.header("Compliance Checklist")

checks = {
    "Dataset Uploaded": True,
    "Model Registered": "model_name" in st.session_state,
    "Fairness Analysis": fairness > 0,
    "Privacy Analysis": privacy > 0,
    "Explainability Analysis": explainability > 0,
    "Accuracy Recorded": accuracy > 0
}

passed = sum(checks.values())
failed = len(checks) - passed

st.session_state["policy_passed"] = passed
st.session_state["policy_failed"] = failed

for item, status in checks.items():

    if status:
        st.success(f"✅ {item}")
    else:
        st.error(f"❌ {item}")

st.metric("Checks Passed", passed)
st.metric("Checks Failed", failed)

st.divider()
# -----------------------------------------------------
# Detailed Assessment
# -----------------------------------------------------

st.header("Detailed Assessment")

assessment = pd.DataFrame({

    "Area": [

        "Fairness",

        "Privacy",

        "Explainability",

        "Accuracy"

    ],

    "Score": [

        fairness,

        privacy,

        explainability,

        accuracy

    ],

    "Status": [

        "PASS" if fairness >= 80 else "REVIEW",

        "PASS" if privacy >= 80 else "REVIEW",

        "PASS" if explainability >= 80 else "REVIEW",

        "PASS" if accuracy >= 80 else "REVIEW"

    ]

})

st.dataframe(

    assessment,

    use_container_width=True,

    hide_index=True

)

st.bar_chart(

    assessment.set_index("Area")["Score"]

)

st.divider()

# -----------------------------------------------------
# Executive Metrics
# -----------------------------------------------------

st.subheader("Executive Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Fairness", f"{fairness:.2f}%")

m2.metric("Privacy", f"{privacy:.2f}%")

m3.metric("Explainability", f"{explainability:.2f}%")

m4.metric("Accuracy", f"{accuracy:.2f}%")

st.divider()

# -----------------------------------------------------
# Recommendations
# -----------------------------------------------------

st.header("Recommendations")

recommendations = []

if fairness < 80:

    recommendations.append(
        "Improve demographic fairness by balancing the training dataset."
    )

if privacy < 80:

    recommendations.append(
        "Increase privacy protection using anonymization or masking."
    )

if explainability < 80:

    recommendations.append(
        "Improve explainability with SHAP/LIME feature importance."
    )

if accuracy < 80:

    recommendations.append(
        "Retrain the model to improve prediction performance."
    )

if len(recommendations) == 0:

    st.success(
        "✅ All Responsible AI checks satisfy enterprise standards."
    )

else:

    for rec in recommendations:

        st.warning(rec)

st.session_state["recommendation_count"] = len(recommendations)

st.divider()

# -----------------------------------------------------
# Deployment Readiness
# -----------------------------------------------------

st.header("Deployment Readiness")

if overall >= 90:

    deployment = "Approved"

    st.success(
        "🟢 Ready for Production Deployment"
    )

elif overall >= 75:

    deployment = "Conditional"

    st.warning(
        "🟡 Deployment Allowed with Minor Improvements"
    )

else:

    deployment = "Rejected"

    st.error(
        "🔴 Deployment Not Recommended"
    )

st.session_state["deployment_status"] = deployment

st.metric(
    "Deployment Status",
    deployment
)

st.divider()

# -----------------------------------------------------
# Enterprise Compliance Status
# -----------------------------------------------------

st.subheader("Enterprise Compliance Status")

c1, c2 = st.columns(2)

c1.metric(
    "Compliance Score",
    f"{overall:.2f}%"
)

c2.metric(
    "Risk Level",
    risk_level
)

if overall >= 90:

    st.success("Enterprise AI System Approved")

elif overall >= 75:

    st.warning("Enterprise AI System Requires Minor Improvements")

else:

    st.error("Enterprise AI System Failed Compliance")

st.divider()

# -----------------------------------------------------
# Save All Results
# -----------------------------------------------------

st.session_state["overall_compliance"] = overall
st.session_state["compliance_score"] = overall
st.session_state["risk_level"] = risk_level
st.session_state["deployment_status"] = deployment
# -----------------------------------------------------
# Generate Enterprise PDF Report
# -----------------------------------------------------

st.header("📄 Generate Compliance Report")

organization = st.text_input(
    "Organization",
    value="AI Guardian OS"
)

analyst = st.text_input(
    "Prepared By",
    value="Developer"
)

report_name = st.text_input(
    "Report Name",
    value="Compliance_Report"
)

generate = st.button(
    "Generate Enterprise PDF",
    type="primary"
)

if generate:

    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )
    import uuid

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    pdf_path = report_dir / f"{report_name}.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>AI Guardian OS</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Enterprise Responsible AI Compliance Report",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1,0.3*inch))

    elements.append(
        Paragraph(
            f"<b>Organization:</b> {organization}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Prepared By:</b> {analyst}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Project:</b> {project_id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Compliance Score:</b> {overall:.2f}%",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Risk Level:</b> {risk_level}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Deployment:</b> {deployment}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,0.25*inch))

    table_data = [

        ["Category","Score"],

        ["Fairness",fairness],

        ["Privacy",privacy],

        ["Explainability",explainability],

        ["Accuracy",accuracy],

        ["Overall",overall]

    ]

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1,0.25*inch))

    elements.append(
        Paragraph(
            "<b>Recommendations</b>",
            styles["Heading2"]
        )
    )

    if len(recommendations)==0:

        elements.append(
            Paragraph(
                "All Responsible AI requirements satisfied.",
                styles["Normal"]
            )
        )

    else:

        for rec in recommendations:

            elements.append(
                Paragraph(
                    "• "+rec,
                    styles["Normal"]
                )
            )

    certificate=str(uuid.uuid4())[:8].upper()

    elements.append(Spacer(1,0.3*inch))

    elements.append(
        Paragraph(
            f"<b>Certificate ID:</b> {certificate}",
            styles["Normal"]
        )
    )

    doc.build(elements)

    st.success("Enterprise Compliance Report Generated Successfully")

    with open(pdf_path,"rb") as pdf:

        st.download_button(

            "⬇ Download PDF",

            pdf,

            pdf_path.name,

            "application/pdf"

        )
# -----------------------------------------------------
# Export Excel Summary
# -----------------------------------------------------

st.header("Export Summary")

excel_buffer = io.BytesIO()

with pd.ExcelWriter(

    excel_buffer,

    engine="openpyxl"

) as writer:

    score_df.to_excel(

        writer,

        sheet_name="Compliance Scores",

        index=False

    )

    assessment.to_excel(

        writer,

        sheet_name="Assessment",

        index=False

    )

st.download_button(

    "⬇ Download Excel Summary",

    excel_buffer.getvalue(),

    "compliance_summary.xlsx",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)

# -----------------------------------------------------
# Completion Status
# -----------------------------------------------------

st.divider()

st.success(

    f"""

Compliance report generation completed successfully.

Project ID: {project_id}

Overall Compliance Score: {overall:.2f}%

Risk Level: {risk_level}

The generated PDF and Excel reports are now available for governance, auditing, and regulatory documentation.

"""

)
st.divider()

st.subheader("Responsible AI Compliance Status")

c1, c2 = st.columns(2)

c1.metric(
    "Compliance Score",
    f"{overall}%"
)

c2.metric(
    "Risk Level",
    risk_level
)

if overall >= 90:
    st.success("🟢 AI System Approved")

elif overall >= 75:
    st.warning("🟡 AI System Requires Minor Improvements")

else:
    st.error("🔴 AI System Not Approved")
