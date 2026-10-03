
import csv
import re


def load_skills(skills_file):
    """
    Load skills from the skills CSV file.

    Parameters:
        skills_file: Path to the skills CSV file.

    Returns:
        A list of skills.
    """

    skills = []

    with open(skills_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skills.append(row["skill"])

    return skills


def extract_skills(text, skills):
    """
    Extract known skills from text.

    Parameters:
        text: Cleaned resume text.
        skills: List of known skills.

    Returns:
        List of detected skills.
    """

    text = text.lower()

    detected_skills = []

    for skill in skills:
        skill_lower = skill.lower()

        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):
            detected_skills.append(skill)

    return detected_skills