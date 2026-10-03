
from src.text_preprocessing import clean_text


def test_clean_text():
    text = "Python     SQL\n\nMachine Learning!!!"

    cleaned_text = clean_text(text)

    assert cleaned_text == "python sql machine learning"       #If you accidentally change the preprocessing code later and the result becomes different, pytest will tell us immediately.
    