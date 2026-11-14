import pytest
import base64
from pydantic import ValidationError
from cv_generator.schemas import Profile, CVSpec, FactForm


def test_minimal_profile():
    profile = Profile(name = "Morten")
    assert profile.name == "Morten"
    assert profile.orcid is None

def test_bad_orcid_profile():
    with pytest.raises(ValidationError):
        Profile(name="Jane Doe", orcid="123-123-123-123")

def test_max_publications():
    qid = FactForm(qid="Q12")
    spec = CVSpec(fact_form = qid, max_publications = 5)
    assert spec.max_publications == 5

    spec = CVSpec(fact_form = qid)
    assert spec.max_publications is None

    with pytest.raises(ValidationError):
        CVSpec(fact_form = qid, max_publications = -1)
        

def make_b64_pdf(content: bytes = b"%PDF-dummy content") -> str:
    return base64.b64encode(content).decode("utf-8")

def test_factform_valid_pdf():
    raw_pdf = b"%PDF-test data"
    b64_str = make_b64_pdf(raw_pdf)
    
    form = FactForm(cv_pdf=b64_str)
    assert form.qid is None
    assert form.cv_pdf == raw_pdf

def test_factform_not_a_pdf():
    not_pdf_b64 = base64.b64encode(b"plain text").decode("utf-8")
    
    with pytest.raises(ValidationError):
        FactForm(cv_pdf=not_pdf_b64)

def test_factform_neither_provided():
    with pytest.raises(ValidationError, match="Provide at least a PDF file or QID."):
        FactForm()


def test_factform_both_provided():
    raw_pdf = b"%PDF-test data"
    b64_str = make_b64_pdf(raw_pdf)
    fact = FactForm(qid="Q42", cv_pdf=b64_str)

    assert fact.qid == "Q42" and fact.cv_pdf == raw_pdf

