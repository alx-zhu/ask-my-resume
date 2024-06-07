import streamlit as st
from datetime import date
from constants import SAMPLE_RESUME
from io import BytesIO
from linkedin_pdf_parser import parse_linkedin_profile_pdf


def form_submit_button(id=""):
    if st.button("Submit", key=f"submit_button_{id}"):
        st.session_state.is_chat_open = True
        st.rerun()


def set_form_fields_from_profile(profile):
    st.session_state.intro = profile["intro"]
    st.session_state.experience = profile["experience"]
    st.session_state.projects = profile["projects"]
    st.session_state.education = profile["education"]


def reset_all_form_fields():
    st.session_state.intro = {
        "name": "",
        "email": "",
        "summary": "",
    }
    st.session_state.experience = []
    st.session_state.projects = []
    st.session_state.education = []


@st.experimental_dialog("Upload Your LinkedIn Profile")
def upload_linkedin_profile():
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        # Read the uploaded file as bytes
        pdf_bytes = uploaded_file.getvalue()
        if st.button("Submit"):
            parsed_profile = parse_linkedin_profile_pdf(BytesIO(pdf_bytes))
            set_form_fields_from_profile(parsed_profile)
            st.rerun()
    st.divider()
    with st.expander("How to export your Linkedin profile"):
        st.markdown("### Exporting Your Profile from LinkedIn")
        st.markdown(
            '1. Navigate to your LinkedIn Profile Page \n2. Click on the "More" Button. \n3. Click "Save to PDF"'
        )
        st.image("import_instructions.png")


def render_form():
    if "intro" not in st.session_state:
        reset_all_form_fields()

    st.title("Create Your Profile")
    introduction_form()
    st.divider()
    experience_form()
    st.divider()
    projects_form()
    st.divider()
    education_form()
    st.divider()

    with st.sidebar:
        if st.button("Import LinkedIn Profile", key="import_from_linkedin"):
            upload_linkedin_profile()

        if st.button("Use Alex's Sample Resume", key="use_sample"):
            set_form_fields_from_profile(SAMPLE_RESUME)
            st.rerun()

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear All", key="clear_all"):
                reset_all_form_fields()
                st.rerun()
        with col2:
            form_submit_button("sidebar")


def introduction_form():
    if "intro" not in st.session_state:
        st.session_state.intro = {
            "name": "",
            "email": "",
            "summary": "",
        }

    st.subheader("Introduction")
    st.session_state.intro["name"] = st.text_input(
        f"Name", value=st.session_state.intro.get("name", ""), key="name"
    )
    st.session_state.intro["email"] = st.text_input(
        f"Email", value=st.session_state.intro.get("email", ""), key="email"
    )
    st.session_state.intro["summary"] = st.text_area(
        f"Summary",
        value=st.session_state.intro.get("summary", "").strip(),
        key="summary",
    )


def experience_form():
    # Initialize session state for storing work experiences
    if "experience" not in st.session_state:
        st.session_state.experience = []

    # Function to add an empty experience form
    def add_experience_form():
        st.session_state.experience.append(
            {
                "title": "",
                "company": "",
                "start": date.today(),
                "end": date.today(),
                "description": "",
            }
        )

    # Display experience forms
    st.subheader("Experience")

    forms_container = st.container()

    # Add experience button
    if st.button("Add Experience"):
        add_experience_form()

    with forms_container:
        for i, experience in enumerate(st.session_state.experience):
            title = (
                f"{experience['title']} @ {experience['company']}"
                if experience["title"]
                else "Untitled Experience"
            )
            with st.expander(title, expanded=True):
                st.session_state.experience[i]["title"] = st.text_input(
                    f"Job Title",
                    value=experience.get("title", ""),
                    key=f"job_title_{i}",
                )
                st.session_state.experience[i]["company"] = st.text_input(
                    f"Company", value=experience.get("company", ""), key=f"company_{i}"
                )
                st.session_state.experience[i]["start"] = st.date_input(
                    f"Start Date",
                    value=experience.get("start", None),
                    key=f"start_date_{i}",
                )
                st.session_state.experience[i]["end"] = st.date_input(
                    f"End Date", value=experience.get("end", None), key=f"end_date_{i}"
                )
                st.session_state.experience[i]["description"] = st.text_area(
                    f"Description",
                    value=experience.get("description", "").strip(),
                    key=f"description_{i}",
                )

                if st.button("Delete", key=f"delete_button_{i}"):
                    del st.session_state.experience[i]
                    st.rerun()


def projects_form():
    # Initialize session state for storing projects
    if "projects" not in st.session_state:
        st.session_state.projects = []

    # Function to add an empty project form
    def add_project_form():
        st.session_state.projects.append(
            {
                "title": "",
                "organization": "",
                "start": date.today(),
                "end": date.today(),
                "description": "",
            }
        )

    # Display project forms
    st.subheader("Projects")

    forms_container = st.container()

    # Add project button
    if st.button("Add Project"):
        add_project_form()

    with forms_container:
        for i, project in enumerate(st.session_state.projects):
            title = project["title"] if project["title"] else "Untitled Project"
            with st.expander(
                title,
                expanded=True,
            ):
                st.session_state.projects[i]["title"] = st.text_input(
                    "Project Title",
                    value=project.get("title", ""),
                    key=f"project_title_{i}",
                )
                st.session_state.projects[i]["organization"] = st.text_input(
                    "Organization",
                    value=project.get("organization", ""),
                    key=f"organization_{i}",
                )
                st.session_state.projects[i]["start"] = st.date_input(
                    "Start Date",
                    value=project.get("start", None),
                    key=f"project_start_date_{i}",
                )
                st.session_state.projects[i]["end"] = st.date_input(
                    "End Date",
                    value=project.get("end", None),
                    key=f"project_end_date_{i}",
                )
                st.session_state.projects[i]["description"] = st.text_area(
                    "Description",
                    value=project.get("description", "").strip(),
                    key=f"project_description_{i}",
                )

                if st.button("Delete", key=f"project_delete_button_{i}"):
                    del st.session_state.projects[i]
                    st.rerun()


def education_form():
    if "education" not in st.session_state:
        st.session_state.education = []

    def add_education_form():
        st.session_state.education.append(
            {
                "school": "",
                "degree": "",
                "start": date.today(),
                "end": date.today(),
                "gpa": 0.0,
                "description": "",
            }
        )
        st.rerun()

    # Display education forms
    st.subheader("Education")

    forms_container = st.container()

    # Add project button
    # Add education button
    if st.button("Add Education"):
        add_education_form()

    with forms_container:
        for i, ed in enumerate(st.session_state.education):
            title = f"{ed.get('degree', '')} @ {ed.get('school', '')}"
            with st.expander(title, expanded=True):
                st.session_state.education[i]["school"] = st.text_input(
                    "School/University",
                    value=ed.get("school", ""),
                    key=f"school_{i}",
                )
                st.session_state.education[i]["degree"] = st.text_input(
                    "Degree", value=ed.get("degree", ""), key=f"degree_{i}"
                )
                st.session_state.education[i]["start"] = st.date_input(
                    "Start Date",
                    value=ed.get("start", None),
                    key=f"ed_start_date_{i}",
                )
                st.session_state.education[i]["end"] = st.date_input(
                    "End Date", value=ed.get("end", None), key=f"ed_end_date_{i}"
                )
                st.session_state.education[i]["gpa"] = st.number_input(
                    "GPA",
                    value=float(ed.get("gpa", 0.0)),
                    key=f"ed_gpa_{i}",
                    min_value=0.0,
                    max_value=5.0,
                    step=0.01,
                )
                st.session_state.education[i]["description"] = st.text_area(
                    "Description",
                    value=ed.get("description", "").strip(),
                    key=f"ed_description_{i}",
                )

                if st.button("Delete", key=f"ed_delete_button_{i}"):
                    del st.session_state.education[i]
                    st.rerun()


# {
#     "intro": {
#         "name": "",
#         "email": "",
#         "summary": "",
#     },
#     "experience": [
#         {
#             "title": "",
#             "company": "",
#             "start": date,
#             "end": date,
#             "description": "",
#         },
#     ],
#     "projects": [
#         {
#             "title": "",
#             "organization": "",
#             "start": date,
#             "end": date,
#             "description": "",
#         }
#     ],
#     "education": [
#         {
#             "school": "",
#             "degree": "",
#             "start": date,
#             "end": date,
#             "gpa": 0.0,
#             "description": "",
#         }
#     ],
# }
