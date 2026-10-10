
import fitz


def extract_text_from_pdf(pdf_source):
    """
    Extract text from a PDF file path or a Streamlit uploaded file.
    """

    try:
        # Handle a Streamlit uploaded file.
        if hasattr(pdf_source, "getvalue"):
            pdf_bytes = pdf_source.getvalue()

            with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
                return "\n".join(
                    page.get_text() for page in document
                )

        # Handle a regular file path.
        with fitz.open(pdf_source) as document:
            return "\n".join(
                page.get_text() for page in document
            )

    except Exception as error:
        raise RuntimeError(
            f"Could not extract text from PDF: {error}"
        ) from error
