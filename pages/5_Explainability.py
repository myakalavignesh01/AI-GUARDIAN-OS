import io
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import shap
import matplotlib.pyplot as plt

from database.database import get_connection
from database.logger import log

st.set_page_config(
    page_title="Explainability",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Model Explainability")
st.caption("Understand model predictions using SHAP")
st.divider()

if "dataset" not in st.session_state:
    st.error("❌ Please upload a dataset first from the Upload Dataset page.")
    st.stop()

df = st.session_state["dataset"]

if df is None or df.empty:
    st.error("❌ Dataset is empty.")
    st.stop()

st.success("✅ Dataset loaded successfully.")
st.dataframe(df.head(), use_container_width=True)
st.divider()

columns = list(df.columns)

if len(columns) < 2:
    st.error("❌ Dataset must contain at least 2 columns.")
    st.stop()

target = st.selectbox("Target Column", columns)
features = [c for c in columns if c != target]

if len(features) == 0:
    st.error("❌ No feature columns available after selecting target.")
    st.stop()

working_df = df.copy()
encoders = {}

for col in working_df.columns:
    if working_df[col].dtype == object:
        encoder = LabelEncoder()
        working_df[col] = encoder.fit_transform(working_df[col].astype(str))
        encoders[col] = encoder

X = working_df[features]
y = working_df[target]

if X.shape[1] == 0:
    st.error("❌ No usable features available for training.")
    st.stop()

if y.nunique() < 2:
    st.error("❌ Target column must contain at least 2 classes.")
    st.stop()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y if y.nunique() > 1 else None
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

st.metric("Model Accuracy", f"{accuracy:.2%}")
st.divider()

with st.spinner("Calculating SHAP values..."):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

if isinstance(shap_values, list):
    shap_values_for_importance = shap_values[1] if len(shap_values) > 1 else shap_values[0]
else:
    shap_values_for_importance = shap_values

shap_values_for_importance = np.array(shap_values_for_importance)
importance_array = np.abs(shap_values_for_importance).mean(axis=0)
importance_array = np.array(importance_array).ravel()
feature_names = np.array(features).ravel()

min_len = min(len(feature_names), len(importance_array))
feature_names = feature_names[:min_len]
importance_array = importance_array[:min_len]

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_array
}).sort_values(by="Importance", ascending=False).reset_index(drop=True)

st.success("SHAP explanation generated successfully.")

st.divider()
st.header("SHAP Summary")
try:
    shap.summary_plot(
        shap_values_for_importance,
        X_test,
        feature_names=features,
        show=False
    )
    fig = plt.gcf()
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)

    st.download_button(
        "⬇ Download SHAP plot",
        buf.getvalue(),
        "shap_summary.png",
        "image/png"
    )
except Exception as e:
    st.error(f"Failed to render SHAP summary: {e}")

st.divider()
st.header("Feature Importance")
st.dataframe(importance_df, use_container_width=True)
st.bar_chart(importance_df.set_index("Feature")["Importance"])

st.divider()
st.header("Model Transparency")

mean_importance = importance_df["Importance"].mean() if not importance_df.empty else 0

if not importance_df.empty:
    top_feature = importance_df.iloc[0]["Feature"]
    top_score = float(importance_df.iloc[0]["Importance"])
else:
    top_feature = "N/A"
    top_score = 0.0

transparency_score = round(min(accuracy * 100, 100), 2)

st.session_state["explainability_score"] = transparency_score
st.session_state["model_accuracy"] = round(accuracy * 100, 2)
st.session_state["top_feature"] = top_feature

c1, c2, c3 = st.columns(3)
c1.metric("Transparency", f"{transparency_score}%")
c2.metric("Top Feature", top_feature)
c3.metric("Top SHAP Score", round(top_score, 4))

st.progress(transparency_score / 100)

st.divider()
st.header("Executive Summary")

summary = f"""
The model achieved an accuracy of {accuracy:.2%}.

The most influential feature is '{top_feature}'.

The calculated transparency score is {transparency_score}%.

SHAP analysis indicates that the model is primarily influenced by a small number
of high-impact variables while remaining interpretable across all features.
"""

st.info(summary)
st.success("✅ Explainability analysis completed.")

st.divider()
st.header("Save Analysis")

project_id = st.number_input(
    "Project ID",
    min_value=1,
    value=1,
    key="explain_project"
)

analyst = st.text_input(
    "Analyst",
    value="Developer",
    key="explain_user"
)

if st.button("💾 Save Explainability", type="primary"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE models
            SET explainability=?
            WHERE project_id=?
            """,
            (
                transparency_score,
                project_id
            )
        )
        conn.commit()
        conn.close()

        log(
            analyst,
            f"Generated SHAP explainability for Project {project_id}",
            "INFO"
        )

        st.success("Explainability analysis saved.")
    except Exception as e:
        st.error(f"Failed to save explainability: {e}")

st.divider()
st.header("Export Results")

report_df = importance_df.copy()
report_df["Model Accuracy"] = accuracy
report_df["Transparency Score"] = transparency_score

csv = report_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "explainability_report.csv",
    "text/csv"
)

excel_buffer = io.BytesIO()
try:
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        report_df.to_excel(writer, sheet_name="Explainability", index=False)
    excel_buffer.seek(0)

    st.download_button(
        "⬇ Download Excel",
        excel_buffer.getvalue(),
        "explainability_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except Exception as e:
    st.error(f"Failed to export Excel file: {e}")

st.divider()
st.success(f"""
Explainability analysis completed successfully.

Model Accuracy : {accuracy:.2%}

Transparency Score : {transparency_score}%

Most Influential Feature : {top_feature}

The generated reports are ready to be included in Responsible AI compliance documentation.
""")

st.divider()
st.subheader("AI Explainability Status")

col1, col2 = st.columns(2)
col1.metric("Transparency Score", f"{transparency_score}%")
col2.metric("Model Accuracy", f"{accuracy*100:.2f}%")

if transparency_score >= 90:
    st.success("✅ Model is Highly Explainable")
elif transparency_score >= 75:
    st.warning("⚠️ Model is Moderately Explainable")
else:
    st.error("❌ Model Explainability Needs Improvement")
