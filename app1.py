import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Simple Chatbot", layout="wide")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Chats")

    if st.button("➕ New Chat"):
        st.session_state.messages = []

# ---------------- MAIN TITLE ----------------
st.title("Simple Chatbot")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    st.success(f"File Uploaded: {uploaded_file.name}")

# ---------------- CHAT HISTORY ----------------
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Simple bot reply (you can replace with Ollama / OCR / AI later)
    bot_reply = "Hello, I am your simple chatbot."

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()