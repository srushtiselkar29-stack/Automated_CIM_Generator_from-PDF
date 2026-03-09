import streamlit as st
import requests
import time
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="CIM Generator",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Custom Styling
# -----------------------------

st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:700;
    color:#1f4e79;
}

.subtitle {
    font-size:18px;
    color:#555;
}

.upload-box {
    border: 2px dashed #ccc;
    padding: 30px;
    border-radius: 10px;
}

.generate-btn button {
    background-color:#1f4e79;
    color:white;
    font-size:18px;
    border-radius:8px;
    height:50px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------

st.markdown('<p class="main-title">Automated CIM Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate a 10-slide Confidential Information Memorandum from Annual Reports</p>', unsafe_allow_html=True)

st.divider()

# -----------------------------
# Upload Section
# -----------------------------

st.markdown("### Upload Annual Report")

uploaded_file = st.file_uploader(
    "Upload PDF Report",
    type=["pdf"]
)

# -----------------------------
# Generate Button
# -----------------------------

generate_clicked = st.button("🚀 Generate PowerPoint")

# -----------------------------
# Backend API Endpoint
# -----------------------------

API_URL = "http://localhost:8000/generate-ppt"

# -----------------------------
# Pipeline Execution
# -----------------------------

if generate_clicked:

    if uploaded_file is None:
        st.warning("Please upload a PDF report first.")

    else:

        st.info("Uploading report and generating CIM...")

        with st.spinner("Generating presentation..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }

            try:

                response = requests.post(API_URL, files=files)

                if response.status_code != 200:
                    st.error("Backend error while generating presentation")
                    st.stop()

                ppt_path = response.json()["ppt_path"]

            except Exception as e:
                st.error(f"Could not connect to backend: {e}")
                st.stop()

        st.success("CIM Generated Successfully")

        # -----------------------------
        # Download Section
        # -----------------------------

        ppt_file = Path(ppt_path)

        if not ppt_file.exists():
            st.error("Generated PPT file not found")
        else:

            with open(ppt_file, "rb") as file:

                st.download_button(
                    label="📥 Download PowerPoint",
                    data=file,
                    file_name="generated_cim.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )