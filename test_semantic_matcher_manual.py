
from src.semantic_matcher import match_resume_semantically


def main():
    resume = """
    Python developer with experience in machine learning,
    data analysis, pandas, and building predictive models.
    """

    jobs = [
        {
            "job_role": "Data Scientist",
            "job_description": (
                "Develop predictive models, analyse datasets, "
                "and apply machine learning techniques."
            ),
        },
        {
            "job_role": "Frontend Developer",
            "job_description": (
                "Build responsive web interfaces using HTML, "
                "CSS, JavaScript, and frontend frameworks."
            ),
        },
    ]

    results = match_resume_semantically(resume, jobs)

    for result in results:
        print(
            f"{result['job_role']}: "
            f"{result['similarity_score']}%"
        )


if __name__ == "__main__":
    main()
