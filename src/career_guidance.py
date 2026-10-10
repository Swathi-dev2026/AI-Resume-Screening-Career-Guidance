
import csv


def load_learning_resources(file_path):
    """Load learning resources from a CSV file."""
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def recommend_learning_resources(missing_skills, resources):
    """Recommend resources for skills the candidate is missing."""
    missing_skill_set = {
        skill.strip().casefold()
        for skill in missing_skills
    }

    recommendations = [
        resource
        for resource in resources
        if resource["skill"].strip().casefold() in missing_skill_set
    ]

    return recommendations
