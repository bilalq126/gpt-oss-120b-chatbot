import streamlit as st
from openai import OpenAI

# --- Setup API Client ---
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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",  # Replace with your own HF key if needed
)

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_role" not in st.session_state:
    st.session_state.system_role = ""

# --- Title ---
st.set_page_config(page_title="GPT-OSS Chat", layout="centered")
st.title("🤖 GPT-OSS-120B Chat with Custom Role")

# --- Role Input (RAG-like) ---
with st.expander("🔧 Set a Custom Role / Behavior"):
    new_role = st.text_area(
        "Define how the AI should behave (e.g., 'You are a helpful tutor who explains concepts simply.')",
        value=st.session_state.system_role,
        placeholder="Enter custom role instructions here..."
    )
    if st.button("Set Role"):
        st.session_state.system_role = new_role.strip()
        st.session_state.messages = []  # reset conversation
        st.success("Custom role set and conversation reset.")

# --- Show Chat History ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Enter your message...")
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Prepare messages for LLM: include system role if available
    messages_for_api = []
    if st.session_state.system_role:
        messages_for_api.append({
            "role": "system",
            "content": st.session_state.system_role
        })
    messages_for_api += st.session_state.messages

    # Get LLM response
    try:
        with st.spinner("Generating response..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b:novita",
                messages=messages_for_api
            )
            reply = response.choices[0].message.content
    except Exception as e:
        reply = f"[Error] {str(e)}"

    # Display and store bot response
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
