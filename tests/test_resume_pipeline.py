
from src.resume_parser import extract_text_from_pdf
from src.text_preprocessing import clean_text
from src.skill_extractor import load_skills, extract_skills


def test_resume_processing_pipeline():
    # Step 1: Extract text from the PDF
    raw_text = extract_text_from_pdf("data/test_resume.pdf")

    # Step 2: Clean the extracted text
    cleaned_text = clean_text(raw_text)

    # Step 3: Load the skill database
    skills = load_skills("data/skills.csv")

    # Step 4: Detect skills in the cleaned text
    detected_skills = extract_skills(cleaned_text, skills)

    # Step 5: Check the results
    assert "Python" in detected_skills
    assert "SQL" in detected_skills
    assert "Machine Learning" in detected_skills