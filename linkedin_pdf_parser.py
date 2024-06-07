import re
from datetime import datetime, date
import pdfplumber
from io import BytesIO
from typing import Union

# text sizes:
# headers 15.75
# job company 12.0
# job title 11.5
# date and location 10.5
# description 10.5

NAME_THRESHOLD = 25.0
SECTION_TITLE_THRESHOLD = 15.0
COMPANY_UNIVERSITY_THRESHOLD = 11.5
JOB_TITLE_THRESHOLD = 11.0
DATE_LOCATION_DESCRIPTION_THRESHOLD = 10.0
DATE_RANGE_REGEX = r"\b([A-Za-z]+ \d{4}) - (([A-Za-z]+ \d{4})|Present)\b"
DATE_FORMAT = "%B %Y"
EMAIL_REGEX = r"\b[a-zA-Z0-9._-]+@[a-zA-Z0-9]+(\.[a-zA-Z]{2,}){1,}\b"


def extract_email(pdf_file: Union[str, BytesIO]):
    with pdfplumber.open(pdf_file) as pdf:
        if len(pdf.pages) > 0:
            page = pdf.pages[0]
            # Crop to the sidebar
            cropped = page.crop((0, 0, page.width / 3, page.height))
            text = cropped.extract_text_simple()
            match = re.search(EMAIL_REGEX, text)
            # Extract and print the first email address found
            if match:
                email = match.group(0)
                return email
            else:
                return ""


def extract_sections(pdf_file: Union[str, BytesIO]):
    page_regex = re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE)
    with pdfplumber.open(pdf_file) as pdf:
        sections = {}
        section_text = []
        # First section is name and headline
        current_section = "headline"
        name = ""
        for page in pdf.pages:
            cropped = page.crop((page.width / 3, 0, page.width, page.height))
            for line in cropped.extract_text_lines():
                if line:
                    size = line["chars"][0]["size"]
                    text = line["text"]
                    if re.match(page_regex, text):
                        continue

                    if size > NAME_THRESHOLD:
                        name = text

                    # New Section Starts
                    elif size > SECTION_TITLE_THRESHOLD:
                        if current_section:
                            sections[current_section] = section_text
                            section_text = []
                        current_section = text.lower()
                    else:
                        section_text.append((text, size))

                    # print(line["text"], size)
    sections[current_section] = section_text
    return name, sections


def extract_headline(headline_lines):
    return " ".join([line for (line, _) in headline_lines])


def extract_summary(summary_lines):
    return " ".join([line for (line, _) in summary_lines])


def extract_experience(experience_lines):
    experience = []
    current = None
    description = ""
    for line, size in experience_lines:
        if size > COMPANY_UNIVERSITY_THRESHOLD:
            if current:
                current["description"] = description
                experience.append(current)
                description = ""
            current = {"company": line}
        elif size > JOB_TITLE_THRESHOLD:
            # New title at the same company
            if "title" in current:
                current["description"] = description
                experience.append(current)
                current = {"company": current["company"]}
                description = ""
            current["title"] = line
        elif size > DATE_LOCATION_DESCRIPTION_THRESHOLD:
            # Date should only come after a job title and before a description
            if "title" in current:
                pattern = DATE_RANGE_REGEX
                match = re.search(pattern, line)
                if match:
                    current["start"] = datetime.strptime(match.group(1), DATE_FORMAT)
                    if match.group(2).lower() == "present":
                        current["end"] = date.today()
                        current["current"] = True
                    else:
                        current["end"] = datetime.strptime(match.group(2), DATE_FORMAT)
                else:
                    description += " " + line
    current["description"] = description
    experience.append(current)
    return experience


def extract_education(education_lines):
    education = []
    current = None
    description = ""
    for line, size in education_lines:
        if size > COMPANY_UNIVERSITY_THRESHOLD:
            if current:
                current["description"] = description
                current["degree"] = current.get("degree", "")
                current["start"] = current.get("start", None)
                current["end"] = current.get("end", None)
                current["gpa"] = 0.0
                education.append(current)
                description = ""
            current = {"school": line}
        elif size > DATE_LOCATION_DESCRIPTION_THRESHOLD:
            # Date should only come after a job title and before a description
            if "school" in current and "degree" not in current:
                degree = ""
                pattern = DATE_RANGE_REGEX
                match = re.search(pattern, line)
                if match:
                    current["start"] = datetime.strptime(match.group(1), DATE_FORMAT)
                    if match.group(2).lower() == "present":
                        current["end"] = date.today()
                        current["current"] = True
                    else:
                        current["end"] = datetime.strptime(match.group(2), DATE_FORMAT)

                    # Get the degree and remove the dot fom the LinkedIn formatting
                    degree = line.split("(")[0].replace("·", "").strip()
                else:
                    degree = line
                    current["start"] = None
                    current["end"] = None
                current["degree"] = degree

            else:
                description += " " + line

    # Barring against education entries that are missing fields
    current["description"] = description
    current["degree"] = current.get("degree", "")
    current["start"] = current.get("start", None)
    current["end"] = current.get("end", None)
    current["gpa"] = 0.0
    education.append(current)
    return education


def parse_linkedin_profile_pdf(pdf_file: Union[str, BytesIO]):
    name, sections = extract_sections(pdf_file)
    return {
        "intro": {
            "name": name,
            "email": extract_email(pdf_file),
            "summary": extract_summary(sections["summary"]),
        },
        "experience": extract_experience(sections["experience"]),
        "projects": [],
        "education": extract_education(sections["education"]),
    }
