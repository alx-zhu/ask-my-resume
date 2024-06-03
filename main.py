import streamlit as st
from form_components import render_form
from chat_components import openai_chat


def main():
    if "is_chat_open" not in st.session_state:
        st.session_state.is_chat_open = False

    if st.session_state.is_chat_open:
        if st.button("Back to My Resume"):
            st.session_state.is_chat_open = False
            st.rerun
        openai_chat()

    else:
        render_form()
        if st.button("Submit"):
            st.session_state.is_chat_open = True
            st.rerun()


if __name__ == "__main__":
    main()
