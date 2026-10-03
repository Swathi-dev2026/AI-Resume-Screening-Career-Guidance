
#Responsible for extracting text from uploaded resume PDF files using PyMuPDF.

import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Parameters:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text from the PDF.
    """
    try:
        with pymupdf.open(pdf_path) as document:
            text = ""

            for page in document:
                text += page.get_text()

        if not text.strip():
            raise ValueError("No readable text was found in the PDF.")

        return text

    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    except Exception as error:
        raise RuntimeError(f"Could not extract text from PDF: {error}")