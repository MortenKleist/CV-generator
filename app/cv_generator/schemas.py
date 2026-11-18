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
    occupations: list[str] | None = Field(default_factory=list)
    fields_of_work: list[str] | None = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    employment: list[Employment] = Field(default_factory=list)
    publication: list[Publication] = Field(default_factory=list)

class FactForm(BaseModel):
    qid: str | None = Field(default=None, pattern=r"^Q[1-9][0-9]*$")
    cv_pdf: Base64Bytes | None = None

    @field_validator("cv_pdf")
    @classmethod
    def validate_pdf_magic_bytes(cls, v: bytes | None) -> bytes | None:
        if v is not None and not v.startswith(b"%PDF-"):
            raise ValueError("Decoded file is not a valid PDF.")
        return v

    @model_validator(mode="after")
    def check_at_least_one(self) -> "FactForm":
        if self.cv_pdf is None and self.qid is None:
            raise ValueError("Provide at least a PDF file or QID.")
        return self

class CVSpec(BaseModel):
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    max_publications: int | None = Field(default=None, gt=0)
    target: str | None = None
    fact_form: FactForm

class CVContent(BaseModel):
    summary: str | None = None
    education_ids: list[UUID] = Field(default_factory=list)
    employment_ids: list[UUID] = Field(default_factory=list)
    publication_ids: list[UUID] = Field(default_factory=list)
    
