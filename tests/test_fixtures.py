from pathlib import Path

import pytest

from cv_generator.schemas import Profile, CVContent

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def profile() -> Profile:
    text = (FIXTURES / "profile.json").read_text()
    return Profile.model_validate_json(text)

@pytest.fixture
def content() -> CVContent:
    text = (FIXTURES / "content.json").read_text()
    return CVContent.model_validate_json(text)

def test_profile_loads(profile):
    assert profile.name == "Bobby"
    assert len(profile.publication) == 4

def test_content_loads(content):
    assert content.summary == "Hire me, PLEASE!!!"
    assert len(content.publication_ids) == 3

def test_content_ids_exist_in_profile(profile, content):
    known_ids = {publication.id for publication in profile.publication}
    for publication_id in content.publication_ids:
        assert publication_id in known_ids

    known_ids = {education.id for education in profile.education}
    for education_id in content.education_ids:
        assert education_id in known_ids

    known_ids = {employment.id for employment in profile.employment}
    for employment_id in content.employment_ids:
        assert employment_id in known_ids

    