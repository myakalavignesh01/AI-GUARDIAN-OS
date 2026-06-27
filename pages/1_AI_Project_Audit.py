import streamlit as st
import zipfile
import tempfile
import os

st.set_page_config(page_title="AI Project Audit", page_icon="📦", layout="wide")

st.title("📦 AI Project Audit")
st.write("Upload an AI project (.zip) for Responsible AI analysis.")

uploaded_zip = st.file_uploader(
    "Upload AI Project (.zip)",
    type=["zip"]
)

if uploaded_zip:

    temp_dir = tempfile.mkdtemp()

    with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    st.success("✅ Project uploaded and extracted successfully!")

    python_files = []
    datasets = []
    notebooks = []
    models = []
    readme = []

    for root, dirs, files in os.walk(temp_dir):

        for file in files:

            path = os.path.join(root, file)

            if file.endswith(".py"):
                python_files.append(path)

            elif file.endswith(".ipynb"):
                notebooks.append(path)

            elif file.endswith(".csv") or file.endswith(".xlsx") or file.endswith(".json"):
                datasets.append(path)

            elif file.endswith(".pkl") or file.endswith(".joblib") or file.endswith(".onnx"):
                models.append(path)

            elif file.lower().startswith("readme"):
                readme.append(path)

    st.subheader("📊 Project Summary")

    col1,col2,col3=st.columns(3)

    col1.metric("🐍 Python Files",len(python_files))
    col2.metric("📊 Datasets",len(datasets))
    col3.metric("🤖 Models",len(models))

    col1,col2=st.columns(2)

    col1.metric("📓 Notebooks",len(notebooks))
    col2.metric("📄 README Files",len(readme))

    st.divider()

    st.subheader("Detected Files")

    with st.expander("🐍 Python Files"):
        for f in python_files:
            st.write(os.path.basename(f))

    with st.expander("📊 Datasets"):
        for f in datasets:
            st.write(os.path.basename(f))

    with st.expander("🤖 Models"):
        for f in models:
            st.write(os.path.basename(f))

    with st.expander("📓 Notebooks"):
        for f in notebooks:
            st.write(os.path.basename(f))

    with st.expander("📄 README"):
        for f in readme:
            st.write(os.path.basename(f))

    st.success("✅ Project scan completed.")

    if st.button("🚀 Start AI Audit"):

        st.session_state["project_uploaded"] = True
        st.session_state["python_files"] = len(python_files)
        st.session_state["datasets"] = len(datasets)
        st.session_state["models"] = len(models)
        st.session_state["notebooks"] = len(notebooks)

        st.switch_page("pages/13_AI_Trust_Certificate.py")
