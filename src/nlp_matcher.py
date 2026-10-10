
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_descriptions(file_path):
    """Load job descriptions from a CSV file."""
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"job_role", "job_description"}
        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError(
                "CSV must contain job_role and job_description columns."
            )

        return [
            {
                "job_role": row["job_role"].strip(),
                "job_description": row["job_description"].strip(),
            }
            for row in reader
            if row["job_role"] and row["job_description"]
        ]


def match_resume_to_jobs(resume_text, job_descriptions):
    """
    Rank job descriptions by TF-IDF cosine similarity.

    Scores measure text similarity, not hiring probability.
    """
    if not resume_text or not resume_text.strip():
        return []

    if not job_descriptions:
        return []

    documents = [
        resume_text.strip(),
        *[
            job["job_description"].strip()
            for job in job_descriptions
        ],
    ]

    if any(not document for document in documents):
        raise ValueError("Resume and job descriptions must not be empty.")

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:],
    )[0]

    results = []

    for job, similarity in zip(job_descriptions, similarities):
        results.append({
            "job_role": job["job_role"],
            "similarity_score": round(float(similarity) * 100, 2),
        })

    results.sort(
        key=lambda result: result["similarity_score"],
        reverse=True,
    )

    return results
