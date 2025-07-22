import fitz  # PyMuPDF
import os
import json
from PIL import Image

def extract_pdf_content(pdf_path, output_folder, json_output_path):
    # Create output folders
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Prepare JSON structure
    content_list = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text()
        page_images = []

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_num+1}_image{img_index+1}.{image_ext}"
            image_path = os.path.join(images_folder, image_filename)

            # Save image
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            page_images.append(image_path)

        # Append to JSON structure
        content_list.append({
            "page": page_num + 1,
            "text": page_text.strip(),
            "images": page_images
        })

    # Save JSON output
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(content_list, json_file, indent=4, ensure_ascii=False)

    print(f"Extraction complete. Data saved to {json_output_path}")

# Example usage
pdf_file = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
output_directory = "output"
json_output_file = "output/structured_content.json"

extract_pdf_content(pdf_file, output_directory, json_output_file)
