from src.skill_extractor import load_skills, extract_skills


def test_extract_normal_skills():
    skills = load_skills("data/skills.csv")

    text = "python sql machine learning pandas numpy power bi"

    detected_skills = extract_skills(text, skills)

    assert detected_skills == [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Power BI",
    ]


def test_extract_special_character_skills():
    skills = load_skills("data/skills.csv")

    text = "I know C++, C#, and Node.js"

    detected_skills = extract_skills(text, skills)

    assert detected_skills == [
        "C++",
        "C#",
        "Node.js",
    ]