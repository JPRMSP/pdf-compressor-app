import fitz  # PyMuPDF
import tempfile

def compress_pdf(input_file, target_size_mb):
    """
    Compresses a PDF by re-saving it with basic optimizations.

    Parameters:
    - input_file: Uploaded file-like object from Streamlit
    - target_size_mb: Target file size in megabytes (approximate)

    Returns:
    - Path to the compressed PDF file
    """
    # Open the original PDF from stream
    doc = fitz.open(stream=input_file.read(), filetype="pdf")

    # Optional: Optimize by removing unused objects
    doc.save("temp_initial.pdf", garbage=4, deflate=True)

    # Reopen to perform further optimization
    optimized_doc = fitz.open("temp_initial.pdf")

    # Compress images by reducing their quality
    for page_index in range(len(optimized_doc)):
        page = optimized_doc[page_index]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            try:
                # Reduce resolution for each image (simulate recompression)
                pix = fitz.Pixmap(optimized_doc, xref)
                if pix.n > 4:  # contains alpha
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix = fitz.Pixmap(pix, 100, 100)  # downscale
                optimized_doc._delete_object(xref)
                new_xref = optimized_doc.insert_image(page.rect, pixmap=pix, overlay=True)
                pix = None
            except Exception:
                pass  # Skip if any image fails

    # Save to temporary file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    optimized_doc.save(temp_output.name, garbage=4, deflate=True)
    optimized_doc.close()

    return temp_output.name
