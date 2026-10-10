
import csv


def load_job_roles(file_path):
    """
    Load job roles and their required skills from a CSV file.
    """
    job_roles = []

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            required_skills = [
                skill.strip()
                for skill in row["required_skills"].split(",")
                if skill.strip()
            ]

            job_roles.append({
                "job_role": row["job_role"].strip(),
                "required_skills": required_skills,
            })

    return job_roles


def match_job_roles(candidate_skills, job_roles):
    """
    Rank job roles based on the percentage of required skills
    found in the candidate's skills.
    """
    candidate_skill_set = {
        skill.strip().casefold()
        for skill in candidate_skills
    }

    results = []

    for role in job_roles:
        required_skills = role["required_skills"]

        matched_skills = [
            skill
            for skill in required_skills
            if skill.casefold() in candidate_skill_set
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill.casefold() not in candidate_skill_set
        ]

        if required_skills:
            match_score = (
                len(matched_skills) / len(required_skills)
            ) * 100
        else:
            match_score = 0.0

        results.append({
            "job_role": role["job_role"],
            "match_score": round(match_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        })

    results.sort(
        key=lambda result: result["match_score"],
        reverse=True,
    )

    return results
