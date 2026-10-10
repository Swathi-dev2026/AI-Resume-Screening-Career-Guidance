
def analyze_skill_gap(candidate_skills, job_role):
    """
    Compare a candidate's skills with a job role's requirements.

    Returns matched skills, missing skills, and skill coverage.
    """

    candidate_skill_set = {
        skill.strip().casefold()
        for skill in candidate_skills
    }

    required_skills = job_role["required_skills"]

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
        coverage = len(matched_skills) / len(required_skills) * 100
    else:
        coverage = 0.0

    return {
        "job_role": job_role["job_role"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round(coverage, 2),
    }
