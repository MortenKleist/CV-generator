Project description
===================

Academic CV generation with LLMs and knowledge graphs
-----------------------------------------------------
Generation of resumé/CV for an academic is often required in connection with
job applications, research grant applications and promotions. One CV
cannot necessarily be reused unmodified between applications, due to
updates and possible restrictions on the format of the CV, e.g., with
respect to number of pages and number of publications that can be
listed. There may be further customizations wanted, file format and
targeted emphasis based on who the CV is for. Some information for a
CV may be readily available in a knowledge graph (Wikidata) while other
information may be necessary to provide in some other form. Large
language models (LLM) has been used for the creation of resumés.

This project should make a Web service that is based on data from a
knowledge graph and some specification about the CV should generate a
CV with an LLM. It is suggested to get the data from Wikidata.

### Scoping questions
- Input: Wikidata, previous CV, target.
- Fielded or free-form restrictions
- Templating
- Output format to support: LaTeX, Markdown, PDF
- Web application: front end for humans to access the Web service.
- Iterative chat or one-off.

### References
* RealCV - An AI-Powered Resume Generator. https://scholia.toolforge.org/work/Q136309845
* CVTool: Automating Content Variants of CVs. https://scholia.toolforge.org/work/Q136309530
* https://resume.io/