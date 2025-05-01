import streamlit as st
from compressor import compress_pdf
from pathlib import Path
import base64

# Page settings
st.set_page_config(page_title="PDF Compressor", layout="centered")

# Function to add background image
def add_bg_from_local(img_file):
    with open(img_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
add_bg_from_local("background.jpg")

# UI Elements
st.title("Nature-Themed PDF Compressor")
st.write("Upload a PDF file, choose the desired file size, and download the compressed version.")

uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
target_size = st.number_input("Target file size (in MB)", min_value=0.1, step=0.1)

if uploaded_pdf and target_size:
    if st.button("Compress PDF"):
        with st.spinner("Compressing... Please wait."):
            output_path = compress_pdf(uploaded_pdf, target_size)
            with open(output_path, "rb") as f:
                st.success("Compression complete!")
                st.download_button(
                    label="Download Compressed PDF",
                    data=f,
                    file_name="compressed.pdf",
                    mime="application/pdf"
                )
