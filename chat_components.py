import time
import streamlit as st
from openai import OpenAI
from constants import OPENAI_INITIAL_CONVERSATION
from keybert import KeyBERT
from rank_projects import rank_projects_by_keyphrases, rank_experiences_by_keyphrases


@st.cache_resource()
def get_cached_openai_service():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def chat_back_button(id=""):
    if st.button("Back to My Resume", key=f"chat_back_button_{id}"):
        st.session_state.is_chat_open = False
        st.session_state.display_conversation = []
        st.session_state.gpt_conversation = []
        st.rerun()


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

    if (
        "gpt_conversation" not in st.session_state
        or len(st.session_state.gpt_conversation) == 0
    ):
        st.session_state.relevant_projects = []
        st.session_state.relevant_experience = []
        st.session_state.gpt_conversation = OPENAI_INITIAL_CONVERSATION
        st.session_state.gpt_conversation.append(
            {
                "role": "system",
                "content": f"You are {name}'s Resume Assistant. Make conversation sound natural, always attribute to {name}. IMPORTANT: Follow the model of the previous conversation. You are a chat assistant LLM whose objective is to ingest the resume of {name} and make conversation with the user to inform them about {name}'s qualifications. Ensure responses are easy to understand, sound natural, and provide details and reasoning behind each response. For example, when providing context about {name}'s experience, explain what they did at each job and why that makes them qualified. Keep responses concise when possible and format with markdown to make the text readable. Include direct references to the experiences, projects, and education provided to help show how {name} is qualified. Note: Do not generate information outside of the context provided. Stick strongly to the experience, projects, education, and introduction given in the context provided! If you do not know the answer to a question, say that you do not know, and to contact {name} directly using the email: {email}. Here is the context about {name}. Introduction: {summary}. Work Experience: {experience}. Projects: {projects}. Education: {education}. You MUST use this information only. Do not add or remove information from what I have provided. To start, introduce yourself like this: Hello! I am [name]'s Resume Assistant! Feel free to ask me any questions about [name]'s work experience, projects, education, and general qualifications. If you aren't sure what to ask, try these:\n 1. Give me a timeline of {name}'s work experience. \n 2. What is {name} most experienced with? \n 3. Give me examples of {name}'s leadership experience.",
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

    with st.sidebar:
        st.subheader("Relevant Projects (from keywords)")
        relevant_projects_placeholder = st.empty()
        st.divider()
        st.subheader("Relevant Experience (from keywords)")
        relevant_experience_placeholder = st.empty()

    # Displaying and updating chat
    st.title("Ask My Resume")

    st.info(
        "#### Thank you for visiting, I'd love your feedback! \n *Please reach out to me at alexanderzhu07@gmail.com with any comments or feedback.*  \n\n **NOTE: This application is a prototype and is still in development.** To keep the project free, users are currently limited to 10 messages."
    )

    for message in st.session_state.display_conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_placeholder = st.empty()
    assistant_placeholder = st.empty()

    # React to user input
    if st.session_state.message_count > 10:
        st.warning(
            "You have passed your limit of 10 messages. In order to keep this service free, there is a 10 message limit per user. Please contact alexanderzhu07@gmail.com with any questions."
        )

    elif prompt := st.chat_input(f"Ask me about {name}!", max_chars=200):
        st.session_state.message_count += 1

        with user_placeholder:
            st.chat_message("user").markdown(prompt)

        st.session_state.display_conversation.append(
            {"role": "user", "content": prompt}
        )
        st.session_state.gpt_conversation.append({"role": "user", "content": prompt})

        with assistant_placeholder:
            with st.spinner("Processing..."):
                # display user keywords
                keyphrase_pairs = get_user_keyphrases()

                # Send message to Open AI
                completion = open_ai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.gpt_conversation,
                )

                response = completion.choices[0].message.content

                # List the most relevant projects and experiences
                st.session_state.relevant_projects = rank_projects_by_keyphrases(
                    st.session_state.projects, keyphrase_pairs
                )[:3]

                print(st.session_state.relevant_projects)
                st.session_state.relevant_experience = rank_experiences_by_keyphrases(
                    st.session_state.experience, keyphrase_pairs
                )[:3]

        # Load relevant projects and experience into the sidebar
        with relevant_projects_placeholder:
            with st.container():
                for rank, project in enumerate(
                    st.session_state.relevant_projects, start=1
                ):
                    with st.expander(f"{rank}. {project['title']}"):
                        st.markdown(f"## {project['title']}")
                        st.markdown(
                            f"#### {project['organization']} (*{project['start']} to {project['end']}*)"
                        )
                        st.markdown(project["description"])

        with relevant_experience_placeholder:
            with st.container():
                for rank, experience in enumerate(
                    st.session_state.relevant_experience, start=1
                ):
                    with st.expander(
                        f"{rank}. {experience['title']} @ {experience['company']}"
                    ):
                        st.markdown(f"## {experience['title']}")
                        st.markdown(
                            f"#### {experience['company']} (*{experience['start']} to {experience['end']}*)"
                        )
                        st.markdown(experience["description"])

        # Display assistant response in chat message container
        full_msg = ""
        with assistant_placeholder:
            for word in response.split(" "):
                full_msg += word + " "
                time.sleep(0.05)
                st.chat_message("assistant").markdown(full_msg)

        # Add assistant response to chat history
        st.session_state.display_conversation.append(
            {"role": "assistant", "content": response}
        )
        st.session_state.gpt_conversation.append(
            {"role": "assistant", "content": response}
        )


def get_user_keyphrases():
    user_messages = " ".join(
        map(
            lambda msg: msg["content"],
            filter(
                lambda msg: msg["role"] == "user", st.session_state.display_conversation
            ),
        )
    )
    kw_model = KeyBERT()
    return kw_model.extract_keywords(
        user_messages,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        # use_maxsum=True,
        top_n=10,
    )[::-1]
    # with st.sidebar:
    #     st.write(keywords)
