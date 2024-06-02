import streamlit as st
from openai import OpenAI
from form_components import experience_form
from chat import openai_chat


@st.cache_resource()
def get_cached_openai_service():
    return OpenAI()


def main():
    if "is_chat_open" not in st.session_state:
        st.session_state.is_chat_open = False

    if st.session_state.is_chat_open:
        openai_chat()

    else:
        experience_form()


if __name__ == "__main__":
    main()
