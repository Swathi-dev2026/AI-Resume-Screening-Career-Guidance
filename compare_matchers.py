
from src.nlp_matcher import match_resume_to_jobs
from src.semantic_matcher import (
    load_semantic_model,
    match_resume_semantically,
)


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
        {
            "job_role": "Data Analyst",
            "job_description": (
                "Analyse business data, prepare reports, "
                "and use Python and data visualisation tools."
            ),
        },
    ]

    # Method 1: Existing TF-IDF matcher
    tfidf_results = match_resume_to_jobs(resume, jobs)

    # Method 2: Semantic matcher
    model = load_semantic_model()
    semantic_results = match_resume_semantically(
        resume,
        jobs,
        model=model,
    )

    print("\n=== TF-IDF MATCHING ===")
    for result in tfidf_results:
        print(
            f"{result['job_role']}: "
            f"{result['similarity_score']}%"
        )

    print("\n=== SEMANTIC MATCHING ===")
    for result in semantic_results:
        print(
            f"{result['job_role']}: "
            f"{result['similarity_score']}%"
        )


if __name__ == "__main__":
    main()
