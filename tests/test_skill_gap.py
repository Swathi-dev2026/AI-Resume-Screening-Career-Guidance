
from src.job_matcher import load_job_roles
from src.skill_gap import analyze_skill_gap


def test_analyze_skill_gap():
    roles = load_job_roles("data/job_roles.csv")

    data_scientist_role = next(
        role
        for role in roles
        if role["job_role"] == "Data Scientist"
    )

    candidate_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
    ]

    result = analyze_skill_gap(
        candidate_skills,
        data_scientist_role,
    )

    assert result["job_role"] == "Data Scientist"
    assert result["skill_coverage"] == 71.43
    assert "Python" in result["matched_skills"]
    assert "Scikit-learn" in result["missing_skills"]


def test_candidate_with_no_skills():
    roles = load_job_roles("data/job_roles.csv")

    result = analyze_skill_gap([], roles[0])

    assert result["matched_skills"] == []
    assert len(result["missing_skills"]) == len(
        roles[0]["required_skills"]
    )
    assert result["skill_coverage"] == 0.0
