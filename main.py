import fitz  # PyMuPDF
import os
import json

def extract_pdf_content(pdf_path, output_folder, json_output_path):
    # Create output folder
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Open PDF
    pdf_document = fitz.open(pdf_path)

    # Prepare JSON structure
    questions_list = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        images = page.get_images(full=True)

        if not images:
            continue  # Skip if no images on the page

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save the image
            image_filename = f"page{page_num+1}_image{img_index+1}.{image_ext}"
            image_path = os.path.join(images_folder, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            # Simulate question and options (placeholder logic)
            question_entry = {
                "question": "What is the next figure?",
                "images": image_path,
                "option_images": []
            }

            # Assume next 2 images as options (you can adjust logic here)
            for option_offset in range(1, 3):
                option_index = img_index + option_offset
                if option_index < len(images):
                    option_xref = images[option_index][0]
                    option_base_image = pdf_document.extract_image(option_xref)
                    option_image_bytes = option_base_image["image"]
                    option_image_ext = option_base_image["ext"]
                    option_filename = f"page{page_num+1}_image{option_index+1}.{option_image_ext}"
                    option_image_path = os.path.join(output_folder, option_filename)

                    # Save option image
                    with open(option_image_path, "wb") as option_img_file:
                        option_img_file.write(option_image_bytes)

                    question_entry["option_images"].append(option_image_path)

            questions_list.append(question_entry)

    # Save JSON output
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(questions_list, json_file, indent=4)

    print(f"Extraction complete. Data saved to {json_output_path}")

# Example usage
pdf_file = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"  # Update to your PDF path
output_directory = "output"
json_output_file = "output/structured_content.json"

extract_pdf_content(pdf_file, output_directory, json_output_file)
