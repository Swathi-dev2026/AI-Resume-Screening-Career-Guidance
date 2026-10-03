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

    matches = []

    # Check longer skills first
    sorted_skills = sorted(skills, key=len, reverse=True)

    for skill in sorted_skills:
        skill_lower = skill.lower()

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill_lower)
            + r"(?![a-z0-9])"
        )

        match = re.search(pattern, text)

        if match:
            matches.append(
                {
                    "skill": skill,
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    # Keep only non-overlapping matches
    selected_matches = []

    for match in matches:
        overlaps = False

        for selected in selected_matches:
            if (
                match["start"] < selected["end"]
                and match["end"] > selected["start"]
            ):
                overlaps = True
                break

        if not overlaps:
            selected_matches.append(match)

    # Sort skills according to their position in the text
    selected_matches.sort(key=lambda item: item["start"])

    return [match["skill"] for match in selected_matches]