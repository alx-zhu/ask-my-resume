import streamlit as st
from form_components import render_form, form_submit_button
from chat_components import openai_chat, chat_back_button


def main():
    if "is_chat_open" not in st.session_state:
        st.session_state.is_chat_open = False

    if st.session_state.is_chat_open:
        chat_back_button("main")
        with st.sidebar:
            chat_back_button("sidebar")
        openai_chat()

    else:
        render_form()
        form_submit_button("main")


if __name__ == "__main__":
    main()
