import fitz  # PyMuPDF
import tempfile
import os

def compress_pdf_to_target_size(input_file, target_size_kb, max_attempts=10):
    """
    Compress a PDF to approximately the given target size (in KB).

    Parameters:
    - input_file: file-like object (e.g. from Streamlit)
    - target_size_kb: desired output size in kilobytes
    - max_attempts: number of compression iterations

    Returns:
    - Path to the compressed PDF
    """
    input_data = input_file.read()
    best_output = None
    best_size = float('inf')

    for quality in range(80, 10, -10):  # progressively lower compression quality
        doc = fitz.open(stream=input_data, filetype="pdf")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        
        # compress=quality helps reduce size by applying more compression
        doc.save(temp_file.name, garbage=4, deflate=True, compress=quality)
        doc.close()

        final_size_kb = os.path.getsize(temp_file.name) / 1024

        if final_size_kb < best_size:
            best_output = temp_file.name
            best_size = final_size_kb

        if final_size_kb <= target_size_kb:
            break  # desired size achieved

    return best_output
