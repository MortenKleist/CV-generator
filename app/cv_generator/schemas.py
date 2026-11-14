from typing import Optional
from pydantic import BaseModel, Field, model_validator, Base64Bytes, field_validator
from uuid import UUID, uuid4

class Education(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    institution: str
    degree: str | None = None
    field_of_study: str | None = None
    start_year: int | None = None
    end_year: int | None = None

class Employment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    employer: str
    position: str | None = None
    start_year: int | None = None
    end_year: int | None = None

class Publication(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    authors: list[str]
    venue: str | None = None
    year: int | None = None
    
class Profile(BaseModel):
    name: str 
    nationality: list[str] = Field(default_factory=list)
    orcid: str | None = Field(default=None, pattern=r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
    wikidata_id: str | None = None
    occupations: list[str] = Field(default_factory=list)
    fields_of_work: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    employment: list[Employment] = Field(default_factory=list)
    publication: list[Publication] = Field(default_factory=list)

class FactForm(BaseModel):
    qid: Optional[str] = Field(default=None, pattern=r"Q[1-9][0-9]*")
    cv_pdf: Optional[Base64Bytes] = None

    @field_validator("cv_pdf")
    @classmethod
    def validate_pdf_magic_bytes(cls, v: Optional[bytes]) -> Optional[bytes]:
        if v is not None and not v.startswith(b"%PDF-"):
            raise ValueError("Decoded file is not a valid PDF.")
        return v

    @model_validator(mode="after")
    def check_one_of(self) -> "FactForm":
        has_pdf = self.cv_pdf is not None 
        has_qid = bool(self.qid is not None)

        if (not has_pdf) == (not has_qid):
            raise ValueError("Provide either a PDF file or QID.")
        return self

class CVspec(BaseModel):
    email: str | None = None
    tlf: str | None = None
    max_publications: int | None = None
    target: str | None = None
    fact_form: FactForm