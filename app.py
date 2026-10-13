
import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.text_preprocessing import clean_text
from src.skill_extractor import load_skills, extract_skills
from src.job_matcher import load_job_roles, match_job_roles
from src.nlp_matcher import (
    load_job_descriptions,
    match_resume_to_jobs,
)
from src.semantic_matcher import (
    load_semantic_model,
    match_resume_semantically,
)
from src.skill_gap import analyze_skill_gap
from src.career_guidance import (
    load_learning_resources,
    recommend_learning_resources,
)


st.set_page_config(
    page_title="AI Resume Screening & Career Guidance",
    page_icon="📄",
    layout="wide",
)

st.title("AI-Powered Resume Screening and Career Guidance Platform")

st.write(
    "Upload your resume to identify skills, explore suitable job roles, "
    "compare job descriptions, analyze skill gaps, and discover "
    "learning resources."
)


# Load the project's reference data.
try:
    skills = load_skills("data/skills.csv")
    job_roles = load_job_roles("data/job_roles.csv")
    job_descriptions = load_job_descriptions(
        "data/job_descriptions.csv"
    )
    learning_resources = load_learning_resources(
        "data/learning_resources.csv"
    )
except (OSError, KeyError, ValueError) as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# Cache the model so it is reused across Streamlit reruns.
@st.cache_resource
def get_semantic_model():
    return load_semantic_model()


uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

if uploaded_file is not None:
    try:
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text or not resume_text.strip():
            st.warning(
                "No readable text was found. "
                "This PDF may be scanned or image-based."
            )
            st.stop()

        cleaned_text = clean_text(resume_text)

        if not cleaned_text or not cleaned_text.strip():
            st.warning(
                "The resume text became empty after preprocessing."
            )
            st.stop()

        detected_skills = extract_skills(cleaned_text, skills)

        # 1. Extracted resume skills
        st.subheader("1. Extracted Resume Skills")

        if detected_skills:
            st.write(", ".join(detected_skills))
        else:
            st.info(
                "No skills from the current skills list were detected."
            )

        # 2. Job role matching based on required skills
        st.subheader("2. Job Role Matches")

        role_results = match_job_roles(
            detected_skills,
            job_roles,
        )

        if role_results:
            st.caption(
                "Scores represent required-skill coverage, "
                "not the probability of getting a job."
            )

            for result in role_results:
                st.markdown(f"**{result['job_role']}**")

                score = result["match_score"]

                st.progress(
                    min(max(score / 100, 0.0), 1.0)
                )
                st.write(f"Skill match: {score:.2f}%")
        else:
            st.info(
                "No job-role matches are available for the "
                "currently detected skills."
            )

        # 3. Job description matching
        st.subheader("3. NLP-Based Job Description Matching")

        matching_method = st.radio(
            "Choose a matching method:",
            options=[
                "TF-IDF",
                "Semantic Matching",
            ],
            horizontal=True,
            help=(
                "TF-IDF compares word importance. Semantic Matching "
                "uses pretrained sentence embeddings."
            ),
        )

        if matching_method == "TF-IDF":
            nlp_results = match_resume_to_jobs(
                cleaned_text,
                job_descriptions,
            )
            score_label = "TF-IDF similarity"

        else:
            with st.spinner(
                "Loading the semantic model and comparing job descriptions..."
            ):
                semantic_model = get_semantic_model()

                nlp_results = match_resume_semantically(
                    cleaned_text,
                    job_descriptions,
                    model=semantic_model,
                )

            score_label = "Semantic similarity"

        st.caption(
            "Similarity scores measure textual similarity. "
            "They are not hiring probabilities or validated "
            "probabilities of job suitability."
        )

        if nlp_results:
            for result in nlp_results:
                st.markdown(f"**{result['job_role']}**")

                score = result["similarity_score"]

                st.progress(
                    min(max(score / 100, 0.0), 1.0)
                )

                st.write(f"{score_label}: {score:.2f}%")
        else:
            st.info(
                "Unable to calculate similarity for the supplied "
                "resume and job descriptions."
            )

        
        # 4. Skill-gap analysis
        st.subheader("4. Skill Gap Analysis")

        if role_results:
            # Use the highest-ranked job role from skill matching.
            best_role_name = role_results[0]["job_role"]

            # Find its full dictionary in the original job-role data.
            best_job_role = next(
                (
                    role
                    for role in job_roles
                    if role["job_role"] == best_role_name
                ),
                None,
            )

            if best_job_role is not None:
                gap = analyze_skill_gap(
                    detected_skills,
                    best_job_role,
                )

                missing_skills = gap["missing_skills"]

                if missing_skills:
                    st.write(
                        f"Skills to develop for **{gap['job_role']}**:"
                    )

                    for skill in missing_skills:
                        st.write(f"- {skill}")
                else:
                    st.success(
                        f"No missing required skills were identified "
                        f"for **{gap['job_role']}**."
                    )

                st.metric(
                    "Required-skill coverage",
                    f"{gap['skill_coverage']:.2f}%",
                )

                # 5. Learning resources
                st.subheader("5. Recommended Learning Resources")

                recommendations = recommend_learning_resources(
                    missing_skills,
                    learning_resources,
                )

                if recommendations:
                    for resource in recommendations:
                        st.markdown(
                            f"**{resource['skill']}** — "
                            f"[{resource['resource_name']}]"
                            f"({resource['resource_url']})"
                        )
                        st.caption(resource["resource_type"])
                else:
                    st.info(
                        "No learning resources are currently listed "
                        "for the identified missing skills."
                    )
            else:
                st.warning(
                    "Could not find the selected job role in "
                    "the job-role reference data."
                )
        else:
            st.info(
                "Skill-gap analysis is unavailable because "
                "no job-role matches were found."
            )

    except Exception as error:
        st.error(
            "Something went wrong while processing this resume. "
            "Please check the error details below."
        )
        st.exception(error)
