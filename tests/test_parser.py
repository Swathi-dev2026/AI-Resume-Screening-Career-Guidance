
from src.resume_parser import extract_text_from_pdf


def test_extract_text_from_pdf():
    text = extract_text_from_pdf("data/test_resume.pdf")

    assert text
    assert "TEST RESUME" in text
    assert "Python" in text
    assert "Machine Learning" in text