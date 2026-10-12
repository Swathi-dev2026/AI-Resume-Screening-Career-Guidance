
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Pretrained model for generating sentence embeddings.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_semantic_model():
    """
    Load and return the pretrained sentence-embedding model.

    The model is downloaded on the first run if it is not cached.
    """
    return SentenceTransformer(MODEL_NAME)


def match_resume_semantically(
    resume_text,
    job_descriptions,
    model=None,
):
    """
    Rank job descriptions by semantic similarity to a resume.

    Args:
        resume_text (str): Extracted text from the resume.
        job_descriptions (list): Dictionaries containing
            'job_role' and 'job_description'.
        model: Optional preloaded SentenceTransformer model.

    Returns:
        list: Job roles ranked by semantic similarity, highest first.

    Note:
        Similarity scores are not hiring probabilities.
    """
    # Handle missing or empty input.
    if not isinstance(resume_text, str) or not resume_text.strip():
        return []

    if not job_descriptions:
        return []

    # Validate and prepare job descriptions.
    job_texts = []

    for job in job_descriptions:
        if not isinstance(job, dict):
            raise ValueError(
                "Each job description must be a dictionary."
            )

        if "job_role" not in job or "job_description" not in job:
            raise ValueError(
                "Each job must contain job_role and job_description."
            )

        description = job["job_description"]

        if not isinstance(description, str) or not description.strip():
            raise ValueError("Job descriptions must not be empty.")

        job_texts.append(description.strip())

    # Load the model only when one has not been supplied.
    if model is None:
        model = load_semantic_model()

    # Encode the resume and job descriptions into embeddings.
    texts = [resume_text.strip(), *job_texts]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Compare the resume embedding with every job embedding.
    similarities = cosine_similarity(
        embeddings[0:1],
        embeddings[1:],
    )[0]

    # Build results using the same structure as the TF-IDF matcher.
    results = []

    for job, similarity in zip(job_descriptions, similarities):
        results.append({
            "job_role": job["job_role"],
            "similarity_score": round(
                float(similarity) * 100,
                2,
            ),
        })

    # Rank the most similar jobs first.
    results.sort(
        key=lambda result: result["similarity_score"],
        reverse=True,
    )

    return results
