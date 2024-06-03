import streamlit as st
from openai import OpenAI
from constants import OPENAI_INITIAL_CONVERSATION
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource()
def get_cached_openai_service():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def openai_chat():
    if not "intro" in st.session_state:
        st.error("Something went wrong. Please reload the page")
        return

    name = st.session_state.intro["name"]
    email = st.session_state.intro["email"]
    summary = st.session_state.intro["summary"]
    experience = st.session_state.experience
    projects = st.session_state.projects
    education = st.session_state.education

    # Initializating
    open_ai = get_cached_openai_service()
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0

    if "display_conversation" not in st.session_state:
        st.session_state.display_conversation = []

    if "gpt_conversation" not in st.session_state:
        st.session_state.gpt_conversation = OPENAI_INITIAL_CONVERSATION

        # Add user's events today to the conversation history befor sending.
        st.session_state.gpt_conversation.append(
            {
                "role": "system",
                "content": f"You are {name}'s Resume Assistant. Make conversation sound natural, always attribute to {name}. IMPORTANT: Follow the model of the previous conversation. You are a chat assistant LLM whose objective is to ingest the resume of {name} and make conversation with the user to inform them about {name}'s qualifications. You should be advertising the person's skillset and experience to recruiters interested in their experience. Ensure responses are easy to understand and provide details and reasoning behind each response. For example, when providing context about {name}'s experience, explain what they did at each job and why that makes them qualified. Keep responses concise when possible and format with markdown to make the text readable. Include direct references to the experiences, projects, and education provided to help show how {name} is qualified. Note: Do not generate information outside of the context provided. Stick strongly to the experience, projects, education, and introduction given in the context provided! If you do not know the answer to a question, say that you do not know, and to contact {name} directly using the email: {email}. Here is the context about {name}. Introduction: {summary}. Work Experience: {experience}. Projects: {projects}. Education: {education}. Reintroduce yourself now, use this new information, and do not do so again afterwards. To start, introduce yourself like this: Hello! I am [name]'s Resume Assistant! Feel free to ask me any questions about [name]'s work experience, projects, education, and general qualifications. If you aren't sure what to ask, try these:\n 1. Give me a timeline of [name]'s work experience. \n 2. What is [name] most experienced with? \n 3. Give me examples of [name]'s leadership experience.",
            },
        )

        completion = open_ai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.gpt_conversation,
        )
        response = completion.choices[0].message.content

        st.session_state.gpt_conversation.append(
            {"role": "assistant", "content": response}
        )
        st.session_state.display_conversation.append(
            {"role": "assistant", "content": response}
        )

    # Displaying and updating chat
    st.title("Ask My Resume")

    for message in st.session_state.display_conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_placeholder = st.empty()
    assistant_placeholder = st.empty()

    # React to user input
    if st.session_state.message_count > 10:
        st.warning(
            "You have passed your limit of 10 messages. In order to keep this service free, there is a 10 message limit per user. Please contact alexanderzhu07@gmail.com for any questions."
        )

    elif prompt := st.chat_input("Message the Scheduling Assistant"):
        st.session_state.message_count += 1
        with user_placeholder:
            st.chat_message("user").markdown(prompt)
            st.session_state.display_conversation.append(
                {"role": "user", "content": prompt}
            )
            st.session_state.gpt_conversation.append(
                {"role": "user", "content": prompt}
            )

            # Send message to Open AI
            completion = open_ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.gpt_conversation,
            )

            response = completion.choices[0].message.content

            # Display assistant response in chat message container
            with assistant_placeholder:
                with st.chat_message("assistant"):
                    # st.write_stream(response_generator(response_msg))
                    st.markdown(response)

            # Add assistant response to chat history
            st.session_state.display_conversation.append(
                {"role": "assistant", "content": response}
            )
            st.session_state.gpt_conversation.append(
                {"role": "assistant", "content": response}
            )
