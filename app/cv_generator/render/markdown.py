from cv_generator.schemas import Profile, CVSpec, CVContent, Education, Employment, Publication

def format_year(start_year: int | None, end_year: int | None) -> str:
    if start_year is not None and end_year is not None:
        return f"{start_year}-{end_year}"
    if start_year is not None:
        return f"{start_year}-"
    if end_year is not None:
        return f"{end_year}"
    return ""


def format_authors(authors: list[str]) -> str:
    return ", ".join(author.strip() for author in authors if author.strip())


def format_education(education: Education) -> str:
    period = format_year(start_year=education.start_year, end_year=education.end_year)
    details = ", ".join(part for part in [education.degree, education.field_of_study] if part)
    parts = [period, education.institution, details]
    line = " — ".join(part for part in parts if part)
    return f"- {line}"


def format_employment(employment: Employment) -> str:
    period = format_year(start_year=employment.start_year, end_year=employment.end_year)
    details = ", ".join(part for part in [employment.employer, employment.position] if part)
    parts = [period, details]
    line = " — ".join(part for part in parts if part)
    return f"- {line}"


def format_publication(publication: Publication) -> str:
    authors = format_authors(publication.authors)
    details = [
        f'"{publication.title}"' if publication.title else "",
        authors,
        publication.venue,
        str(publication.year) if publication.year is not None else ""
        ]
    line = ", ".join(part for part in details if part)
    return f"- {line}"

def render_education(profile: Profile, content: CVContent) -> str:
    by_id = {education.id: education for education in profile.education}
    entries = []

    for education_id in content.education_ids:
        education = by_id.get(education_id)
        if education is None:
            continue
        entries.append(format_education(education))

    if not entries:
        return ""

    return "## Education\n\n" + "\n".join(entries)

def render_employment(profile: Profile, content: CVContent) -> str:
    by_id = {employment.id: employment for employment in profile.employment}
    entries = []

    for employment_id in content.employment_ids:
        employment = by_id.get(employment_id)
        if employment is None:
            continue
        entries.append(format_employment(employment))

    if not entries:
        return ""

    return "## Employment\n\n" + "\n".join(entries)

def render_publication(profile: Profile, content: CVContent) -> str:
    by_id = {publication.id: publication for publication in profile.publication}
    entries = []

    for publication_id in content.publication_ids:
        publication = by_id.get(publication_id)
        if publication is None:
            continue
        entries.append(format_publication(publication))

    if not entries:
        return ""

    return "## Publication\n\n" + "\n".join(entries)


def render_markdown(profile: Profile, content: CVContent, spec: CVSpec | None = None) -> str: 
    sections = []

    # Header
    header = [f"# {profile.name}"]

    if spec and spec.target:
        header.append(f"**{spec.target}**")
    elif profile.occupations:
        header.append(" | ".join(profile.occupations))

    contact = []

    if spec:
        if spec.email:
            contact.append(spec.email)
        if spec.phone:
            contact.append(spec.phone)
        if spec.address:
            contact.append(spec.address)

    if profile.orcid:
        contact.append(f"ORCID: {profile.orcid}")

    if contact:
        header.append(" · ".join(contact))

    sections.append("\n\n".join(header))

    # Professional summary
    if content.summary:
        sections.append(
            "## Profile\n\n" + content.summary
        )

    # Fields of work
    if profile.fields_of_work:
        fields = ", ".join(profile.fields_of_work)

        if fields:
            sections.append(
                "## Areas of Expertise\n\n" + fields
            )

    # Education
    education = render_education(profile, content)
    if education:
        sections.append(education)

    # Employment
    employment = render_employment(profile, content)
    if employment:
        sections.append(employment)

    # Publications
    publications = render_publication(profile, content)

    if publications:
        if spec and spec.max_publications is not None:
            publication_lines = publications.splitlines()
            publication_lines = publication_lines[
                :spec.max_publications + 2
            ]
            publications = "\n".join(publication_lines)

        sections.append(publications)

    return "\n\n".join(sections)

