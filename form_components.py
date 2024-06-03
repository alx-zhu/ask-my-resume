import streamlit as st
from datetime import date
from constants import SAMPLE_RESUME

def render_form():
    if SAMPLE_RESUME and "intro" not in st.session_state:
        st.session_state.intro = SAMPLE_RESUME["intro"]
        st.session_state.experience = SAMPLE_RESUME["experience"]
        st.session_state.projects = SAMPLE_RESUME["projects"]
        st.session_state.education = SAMPLE_RESUME["education"]
    st.title("Create Your Profile")
    introduction_form()
    st.divider()
    experience_form()
    st.divider()
    projects_form()
    st.divider()
    education_form()

def introduction_form():
    if "intro" not in st.session_state:
        st.session_state.intro = {
            "name": "",
            "email": "",
            "summary": "",
        }
    
    st.subheader("Introduction")
    st.session_state.intro["name"] = st.text_input(f"Name", value=st.session_state.intro["name"], key="name")
    st.session_state.intro["email"] = st.text_input(f"Email", value=st.session_state.intro["email"], key="email")
    st.session_state.intro["summary"] = st.text_area(f"Summary", value=st.session_state.intro["summary"], key="summary")


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

    for i, experience in enumerate(st.session_state.experience):
        with st.expander(f"{f"{experience["title"]} @ {experience["company"]}" if experience["title"] else "Untitled Experience"}", expanded=True):
            st.session_state.experience[i]["title"] = st.text_input(
                f"Job Title",
                value=experience["title"],
                key=f"job_title_{i}",
            )
            st.session_state.experience[i]["company"] = st.text_input(
                f"Company", value=experience["company"], key=f"company_{i}"
            )
            st.session_state.experience[i]["start"] = st.date_input(
                f"Start Date",
                value=experience["start"],
                key=f"start_date_{i}",
            )
            st.session_state.experience[i]["end"] = st.date_input(
                f"End Date", value=experience["end"], key=f"end_date_{i}"
            )
            st.session_state.experience[i]["description"] = st.text_area(
                f"Description",
                value=experience["description"],
                key=f"description_{i}",
            )

            if st.button("Delete", key=f"delete_button_{i}"):
                del st.session_state.experience[i]
                st.rerun()

    # Add experience button
    if st.button("Add Experience"):
        add_experience_form()

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

    for i, project in enumerate(st.session_state.projects):
        with st.expander(f"{project['title'] if project["title"] else "Untitled Project"}", expanded=True):
            st.session_state.projects[i]["title"] = st.text_input(
                "Project Title",
                value=project["title"],
                key=f"project_title_{i}",
            )
            st.session_state.projects[i]["organization"] = st.text_input(
                "Organization", value=project["organization"], key=f"organization_{i}"
            )
            st.session_state.projects[i]["start"] = st.date_input(
                "Start Date",
                value=project["start"],
                key=f"project_start_date_{i}",
            )
            st.session_state.projects[i]["end"] = st.date_input(
                "End Date", value=project["end"], key=f"project_end_date_{i}"
            )
            st.session_state.projects[i]["description"] = st.text_area(
                "Description",
                value=project["description"],
                key=f"project_description_{i}",
            )

            if st.button("Delete", key=f"project_delete_button_{i}"):
                del st.session_state.projects[i]
                st.rerun()

    # Add project button
    if st.button("Add Project"):
        add_project_form()


def education_form():
    if "education" not in st.session_state:
        st.session_state.education = []

    def add_education_form():
        st.session_state.education.append({
            "school": "",
            "degree": "",
            "start": date.today(),
            "end": date.today(),
            "gpa": 0.0,
            "description": "",
        })

    # Display education forms
    st.subheader("Education")

    for i, ed in enumerate(st.session_state.education):
        with st.expander(f"{ed["degree"]} @ {ed['school']}", expanded=True):
            st.session_state.education[i]["school"] = st.text_input(
                "School/University",
                value=ed["school"],
                key=f"school_{i}",
            )
            st.session_state.education[i]["degree"] = st.text_input(
                "Degree", value=ed["degree"], key=f"degree_{i}"
            )
            st.session_state.education[i]["start"] = st.date_input(
                "Start Date",
                value=ed["start"],
                key=f"ed_start_date_{i}",
            )
            st.session_state.education[i]["end"] = st.date_input(
                "End Date", value=ed["end"], key=f"ed_end_date_{i}"
            )
            st.session_state.education[i]["gpa"] = st.number_input(
                "GPA", value = float(ed["gpa"]), key=f"ed_gpa_{i}", min_value=0.0, max_value=5.0, step=0.01
            )
            st.session_state.education[i]["description"] = st.text_area(
                "Description",
                value=ed["description"],
                key=f"ed_description_{i}",
            )

            if st.button("Delete", key=f"ed_delete_button_{i}"):
                del st.session_state.education[i]
                st.rerun()
    
    # Add education button
    if st.button("Add Education"):
        add_education_form()

