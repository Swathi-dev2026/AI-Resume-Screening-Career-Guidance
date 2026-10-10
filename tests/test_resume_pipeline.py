
from src.resume_parser import extract_text_from_pdf
from src.text_preprocessing import clean_text
from src.skill_extractor import load_skills, extract_skills
from src.job_matcher import load_job_roles, match_job_roles


def test_resume_processing_pipeline():
    # Step 1: Extract text from the PDF
    raw_text = extract_text_from_pdf("data/test_resume.pdf")

    # Step 2: Clean the extracted text
    cleaned_text = clean_text(raw_text)

    # Step 3: Load the skill database
    skills = load_skills("data/skills.csv")

    # Step 4: Extract skills from the resume
    detected_skills = extract_skills(cleaned_text, skills)

    # Step 5: Load the job-role database
    job_roles = load_job_roles("data/job_roles.csv")

    # Step 6: Match extracted skills to job roles
    matched_roles = match_job_roles(detected_skills, job_roles)

    # Step 7: Verify the pipeline results
    assert "Python" in detected_skills
    assert "SQL" in detected_skills
    assert "Machine Learning" in detected_skills

    assert len(matched_roles) == 6
    assert matched_roles[0]["job_role"] == "Data Scientist"
    assert matched_roles[0]["match_score"] > 0
