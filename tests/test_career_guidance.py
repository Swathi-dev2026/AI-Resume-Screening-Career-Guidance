
from src.career_guidance import (
    load_learning_resources,
    recommend_learning_resources,
)


def test_load_learning_resources():
    resources = load_learning_resources(
        "data/learning_resources.csv"
    )

    assert len(resources) > 0
    assert any(
        resource["skill"] == "Python"
        for resource in resources
    )


def test_recommend_resources_for_missing_skills():
    resources = load_learning_resources(
        "data/learning_resources.csv"
    )

    recommendations = recommend_learning_resources(
        ["Python", "SQL"],
        resources,
    )

    recommended_skills = [
        resource["skill"]
        for resource in recommendations
    ]

    assert "Python" in recommended_skills
    assert "SQL" in recommended_skills


def test_no_matching_resources():
    resources = load_learning_resources(
        "data/learning_resources.csv"
    )

    recommendations = recommend_learning_resources(
        ["Unknown Skill"],
        resources,
    )

    assert recommendations == []
