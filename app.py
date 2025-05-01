import streamlit as st
import os
from compressor import compress_pdf_to_target_size
import base64

# Set page config
st.set_page_config(page_title="PDF Compressor", layout="centered")

# Background image via base64
def add_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set your background image (change the path if needed)
add_bg_image("background.png")  # Use an actual image file in the same folder

# App title
st.title("PDF Compressor")
st.subheader("Compress your PDF to a desired file size")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Size input
unit = st.selectbox("Select unit", ["KB", "MB"])
target_size = st.number_input(f"Target file size ({unit})", min_value=10)

if unit == "MB":
    target_size_kb = target_size * 1024
else:
    target_size_kb = target_size

if uploaded_file and target_size:
    if st.button("Compress PDF"):
        st.info("Compressing... Please wait.")
        original_size_kb = uploaded_file.size / 1024

        try:
            compressed_path = compress_pdf_to_target_size(uploaded_file, target_size_kb)

            final_size_kb = os.path.getsize(compressed_path) / 1024

            st.success(f"Successfully compressed from {original_size_kb:.2f} KB to {final_size_kb:.2f} KB")

            # Download compressed PDF
            with open(compressed_path, "rb") as f:
                compressed_bytes = f.read()

            st.download_button(
                label="Download Compressed PDF",
                data=compressed_bytes,
                file_name="compressed.pdf",
                mime="application/pdf"
            )

            os.remove(compressed_path)

        except Exception as e:
            st.error(f"Compression failed: {e}")
