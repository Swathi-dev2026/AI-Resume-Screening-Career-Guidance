
from src.job_matcher import load_job_roles, match_job_roles


def test_load_job_roles():
    roles = load_job_roles("data/job_roles.csv")

    assert len(roles) == 6
    assert roles[0]["job_role"] == "Data Analyst"
    assert "SQL" in roles[0]["required_skills"]


def test_match_job_roles():
    roles = load_job_roles("data/job_roles.csv")

    candidate_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
    ]

    results = match_job_roles(candidate_skills, roles)

    assert len(results) == 6
    assert results[0]["job_role"] == "Data Scientist"
    assert results[0]["match_score"] == 71.43
    assert "Scikit-learn" in results[0]["missing_skills"]


def test_no_candidate_skills():
    roles = load_job_roles("data/job_roles.csv")

    results = match_job_roles([], roles)

    assert all(result["match_score"] == 0.0 for result in results)
