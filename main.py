import streamlit as st
from form_components import render_form
from chat import openai_chat


def main():
    if "is_chat_open" not in st.session_state:
        st.session_state.is_chat_open = False

    if st.session_state.is_chat_open:
        openai_chat()

    else:
        render_form()


if __name__ == "__main__":
    main()
