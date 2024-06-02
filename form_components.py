import streamlit as st
from datetime import date

def experience_form():
    # Initialize session state for storing work experiences
    if "work_experiences" not in st.session_state:
        st.session_state.work_experiences = []

    # Function to add an empty experience form
    def add_experience_form():
        st.session_state.work_experiences.append(
            {
                "Job Title": "Title",
                "Company": "Company",
                "Start Date": date.today(),
                "End Date": date.today(),
                "Description": "",
            }
        )

    # Add experience button
    if st.button("Add Experience"):
        add_experience_form()

    # Display experience forms
    st.title("Resume Builder")

    for i, experience in enumerate(st.session_state.work_experiences):
        with st.expander(f"{experience["Job Title"]} @ {experience["Company"]}", expanded=True):
            st.session_state.work_experiences[i]["Job Title"] = st.text_input(
                f"Job Title",
                value=experience["Job Title"],
                key=f"job_title_{i}",
            )
            st.session_state.work_experiences[i]["Company"] = st.text_input(
                f"Company", value=experience["Company"], key=f"company_{i}"
            )
            st.session_state.work_experiences[i]["Start Date"] = st.date_input(
                f"Start Date",
                value=experience["Start Date"],
                key=f"start_date_{i}",
            )
            st.session_state.work_experiences[i]["End Date"] = st.date_input(
                f"End Date", value=experience["End Date"], key=f"end_date_{i}"
            )
            st.session_state.work_experiences[i]["Description"] = st.text_area(
                f"Description",
                value=experience["Description"],
                key=f"description_{i}",
            )

    # Display the entered work experiences
    if st.session_state.work_experiences:
        with st.sidebar:
            st.subheader("Work Experiences Summary")
            for i, experience in enumerate(st.session_state.work_experiences):
                with st.container():
                    st.write(f"### Experience {i+1}")
                    st.write(f"**Job Title:** {experience['Job Title']}")
                    st.write(f"**Company:** {experience['Company']}")
                    st.write(f"**Start Date:** {experience['Start Date']}")
                    st.write(f"**End Date:** {experience['End Date']}")
                    st.write(f"**Description:** {experience['Description']}")
                    st.write("---")

def education_form():
    pass
