import os

import google.generativeai as gen_ai
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from streamlit_modal import Modal

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")


def translate_role_for_streamlit(user_role):
    return "assistant" if user_role != "model" else user_role


def translate_role_emoji(user_role):
    return "🤖" if user_role != "model" else "🧑"


def create_chatbot(page_title, site_context, bot_name="OrgrodutBot"):
    st.title(f"🤖 {bot_name}")

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(
            history=[{"role": "user", "parts": site_context}]
        )

    for message in st.session_state.chat_session.history:
        with st.chat_message(
            translate_role_for_streamlit(message.role),
            avatar=translate_role_emoji(message.role),
        ):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input(f"Ask {bot_name}...")
    if user_prompt:
        st.chat_message("user", avatar="🧑").markdown(user_prompt)

        with st.status("Thinking...", expanded=True) as status:
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(gemini_response.text)

            status.update(label="Done", state="complete", expanded=True)

    return st.session_state.chat_session


# Usage in the main chatbot page
if __name__ == "__main__":
    st.set_page_config(
        page_title="Chat with OgrodutBot!",
        page_icon=":brain:",
        layout="centered",
    )

    site_context = """
    Welcome to OgrodutBot! This site provides insights on greenhouse gas emissions, 
    exploring both natural causes like volcanic eruptions and human activities 
    such as industrialization, deforestation, and fossil fuel burning. 
    The goal is to promote awareness and understanding of global warming and climate change.
    """

    create_chatbot("Chat with OgrodutBot!", site_context)
