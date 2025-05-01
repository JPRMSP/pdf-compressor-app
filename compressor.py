import fitz  # PyMuPDF
import tempfile
import os

def compress_pdf_to_target_size(input_file, target_size_kb, max_attempts=10):
    input_data = input_file.read()
    best_output = None
    best_size = float('inf')

    for scale in range(10, max_attempts + 1):
        doc = fitz.open(stream=input_data, filetype="pdf")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        # Resize images in each page to simulate compression
        for page in doc:
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                if base_image:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n > 4:  # CMYK or special
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    # Resize to 80% on each iteration
                    new_pix = pix.scaled(pix.width * (1 - scale * 0.05), pix.height * (1 - scale * 0.05))
                    doc._delete_object(xref)
                    new_xref = doc.insert_image(page.rect, pixmap=new_pix)
                    pix = None
                    new_pix = None

        doc.save(temp_file.name, garbage=4, deflate=True)
        doc.close()

        final_size_kb = os.path.getsize(temp_file.name) / 1024
        if final_size_kb < best_size:
            best_output = temp_file.name
            best_size = final_size_kb

        if final_size_kb <= target_size_kb:
            break

    return best_output
