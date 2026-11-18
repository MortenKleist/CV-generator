import pytest
from pathlib import Path
from cv_generator.render.markdown import format_year, format_authors, format_publication, render_education, render_employment, render_publication
from cv_generator.schemas import Publication, Profile, CVContent


def test_format_authors():
    assert format_authors(["John Michael Smith"]) == "John Michael Smith"
    assert format_authors(["McDonald", "von Neumann"]) == (
        "McDonald, von Neumann"
    )
    assert format_authors(["Jean-Luc Picard"]) == "Jean-Luc Picard"
    assert format_authors([]) == ""


def test_format_year():
    assert format_year(2020, 2024) == "2020-2024"
    assert format_year(2020, None) == "2020-"
    assert format_year(None, 2024) == "2024"
    assert format_year(None, None) == ""


def test_format_publication_missing_details():
    publication = Publication(
        title="Title2",
        authors=[],
        venue=None,
        year=None,
    )

    assert format_publication(publication) == '- "Title2"'


FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def profile() -> Profile:
    text = (FIXTURES / "profile.json").read_text()
    return Profile.model_validate_json(text)

@pytest.fixture
def content() -> CVContent:
    text = (FIXTURES / "content.json").read_text()
    return CVContent.model_validate_json(text)

def test_render_education(profile, content):
    result = render_education(profile, content)

    expected = (
        "## Education\n\n"
        "- DTU — Msc Human Centered AI\n"
        "- 2025 — DTU — Bsc Electrical Engineering"
    )

    assert result == expected

def test_render_employment(profile, content):
    result = render_employment(profile, content)

    expected = (
        "## Employment\n\n"
        "- Job1, Engineer1\n"
        "- Job2\n"
        "- Job3"
    )

    assert result == expected

def test_render_publication(profile, content):
    result = render_publication(profile, content)

    expected = (
        "## Publication\n\n"
        "- \"Title4\", Albert Einstein, Niels Bohr\n"
        "- \"Title1\", Author1, Author2, Venue1\n"
        "- \"Title2\", Author1, Author2"
    )

    assert result == expected
