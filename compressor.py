import fitz  # PyMuPDF
import tempfile
import os

def compress_pdf_to_target_size(input_file, target_size_kb, max_passes=10):
    """
    Compress the input PDF to approximately the target size (in KB).
    Returns the path to the compressed PDF.
    """
    # Save uploaded file to temp file
    input_data = input_file.read()
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_input.write(input_data)
    temp_input.close()

    best_output = None
    best_size = float("inf")

    for _ in range(max_passes):
        doc = fitz.open(temp_input.name)
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        # Save with cleanup and compression options
        doc.save(temp_output.name, garbage=4, deflate=True, clean=True)
        doc.close()

        output_size_kb = os.path.getsize(temp_output.name) / 1024

        # Track smallest size so far
        if output_size_kb < best_size:
            best_output = temp_output.name
            best_size = output_size_kb

        if output_size_kb <= target_size_kb:
            break  # Stop if within target

        # Use output as new input for next pass
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(temp_output.name, "rb") as f:
            temp_input.write(f.read())
        temp_input.close()

    return best_output
