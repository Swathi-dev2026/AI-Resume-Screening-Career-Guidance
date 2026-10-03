
import re


def clean_text(text):
    """
    Clean raw resume text for further NLP processing.

    Parameters:
        text: Raw extracted resume text.

    Returns:
        Cleaned text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Replace multiple spaces and line breaks with one space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary special characters
    text = re.sub(r"[^a-z0-9\s+#.-]", "", text)

    # Remove extra spaces from beginning and end
    text = text.strip()

    return text
