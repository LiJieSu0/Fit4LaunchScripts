import PyPDF2
import os

def extract_text_from_page(input_pdf_path, page_number):
    """
    Extracts text from a specific page of a PDF file.
    page_number is 0-indexed for PyPDF2.
    """
    try:
        with open(input_pdf_path, 'rb') as infile:
            reader = PyPDF2.PdfReader(infile)
            if page_number < len(reader.pages):
                page = reader.pages[page_number]
                text = page.extract_text()
                print(f"Text extracted from page {page_number + 1}:\n{text}")
                return text
            else:
                print(f"Page {page_number + 1} does not exist in the PDF.")
                return None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

if __name__ == "__main__":
    input_pdf = "FPT Report-TMO.pdf"
    # The user wants the first page, which is 0-indexed for PyPDF2
    page_to_extract_text = 0
    extracted_text = extract_text_from_page(input_pdf, page_to_extract_text)

    # Optionally save the extracted text to a file for easier analysis
    if extracted_text:
        output_text_file = "Scripts/extracted_fpt_report_page1_text.txt"
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"Extracted text saved to {output_text_file}")
