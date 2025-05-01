import streamlit as st
from compressor import compress_pdf_to_target_size
import os

# Set page config
st.set_page_config(page_title="PDF Compressor", layout="centered")

# Add background image via custom CSS
def set_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1498050108023-c5249f4df085");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_from_url()

# Title and description
st.title("PDF Compressor")
st.markdown("Compress your PDF to a target size (in KB or MB).")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# Choose target size
unit = st.selectbox("Select Size Unit", ["MB", "KB"])
target_size = st.number_input(f"Enter Target Size ({unit})", min_value=1.0)

if unit == "MB":
    target_size_kb = target_size * 1024
else:
    target_size_kb = target_size

# Compress button
if uploaded_file and target_size_kb:
    if st.button("Compress PDF"):
        with st.spinner("Compressing... please wait"):
            compressed_path = compress_pdf_to_target_size(uploaded_file, target_size_kb)
            final_size_kb = os.path.getsize(compressed_path) / 1024

            st.success(f"Compression complete! Final size: {final_size_kb:.2f} KB")
            with open(compressed_path, "rb") as f:
                st.download_button("Download Compressed PDF", f, file_name="compressed.pdf")
