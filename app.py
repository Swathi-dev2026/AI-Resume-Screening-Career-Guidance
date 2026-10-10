
import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.text_preprocessing import clean_text
from src.skill_extractor import load_skills, extract_skills
from src.job_matcher import load_job_roles, match_job_roles
from src.nlp_matcher import (
    load_job_descriptions,
    match_resume_to_jobs,
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
    "analyze skill gaps, and discover learning resources."
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

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

if uploaded_file is not None:
    try:
        resume_text = extract_text_from_pdf(uploaded_file)
        cleaned_text = clean_text(resume_text)
        detected_skills = extract_skills(cleaned_text, skills)

        if not cleaned_text.strip():
            st.warning(
                "No readable text was found. "
                "This PDF may be scanned or image-based."
            )
            st.stop()

        st.subheader("1. Extracted Resume Skills")

        if detected_skills:
            st.write(", ".join(detected_skills))
        else:
            st.info(
                "No skills from the current skills list were detected."
            )

        st.subheader("2. Job Role Matches")

        role_results = match_job_roles(detected_skills, job_roles)

        if role_results:
            st.caption(
                "Scores represent required-skill coverage, "
                "not the probability of getting a job."
            )

            for result in role_results:
                st.markdown(f"**{result['job_role']}**")
                st.progress(
                    min(max(result["match_score"] / 100, 0.0), 1.0)
                )
                st.write(f"Skill match: {result['match_score']:.2f}%")

        st.subheader("3. NLP-Based Job Description Matching")

        st.caption(
            "These scores measure textual similarity between your resume "
            "and each job description. They are not hiring probabilities."
        )

        nlp_results = match_resume_to_jobs(
            cleaned_text,
            job_descriptions,
        )

        if nlp_results:
            for result in nlp_results:
                st.markdown(f"**{result['job_role']}**")
                st.progress(
                    min(
                        max(result["similarity_score"] / 100, 0.0),
                        1.0,
                    )
                )
                st.write(
                    f"Text similarity: "
                    f"{result['similarity_score']:.2f}%"
                )
        else:
            st.info(
                "Unable to calculate text similarity. "
                "Please provide a resume with readable text."
            )

            st.metric(
                "Required-skill coverage",
                f"{gap['skill_coverage']:.2f}%",
            )

            st.subheader("4. Recommended Learning Resources")

            recommendations = recommend_learning_resources(
                gap["missing_skills"],
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
                    "for the missing skills."
                )

    except Exception as error:
        st.error(
            "Something went wrong while processing this resume. "
            "Please check that the PDF is readable."
        )
        st.exception(error)
