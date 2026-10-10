
import pytest

from src.nlp_matcher import (
    load_job_descriptions,
    match_resume_to_jobs,
)


def test_load_job_descriptions():
    jobs = load_job_descriptions("data/job_descriptions.csv")

    assert len(jobs) == 6
    assert jobs[0]["job_role"] == "Data Analyst"
    assert jobs[0]["job_description"]


def test_match_resume_to_jobs():
    jobs = load_job_descriptions("data/job_descriptions.csv")

    resume_text = (
        "Python SQL statistics machine learning Pandas "
        "NumPy Scikit-learn predictive models"
    )

    results = match_resume_to_jobs(resume_text, jobs)

    assert len(results) == 6
    assert results[0]["job_role"] == "Data Scientist"
    assert 0 <= results[0]["similarity_score"] <= 100


def test_empty_resume_returns_no_results():
    jobs = load_job_descriptions("data/job_descriptions.csv")

    assert match_resume_to_jobs("   ", jobs) == []


def test_empty_job_list_returns_no_results():
    assert match_resume_to_jobs("Python and SQL", []) == []


def test_invalid_csv_header(tmp_path):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        "title,description\nData Scientist,Analyze data\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="CSV must contain"):
        load_job_descriptions(str(csv_file))
