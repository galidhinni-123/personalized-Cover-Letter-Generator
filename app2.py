import streamlit as st
import requests
import uuid

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Simple Chatbot", layout="wide")

# ---------------- OLLAMA FUNCTION ----------------
def ask_ollama(messages):

    url = "http://localhost:11434/api/chat"

    payload = {
        "model": "llama3",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]

    except Exception as e:
        return f"Error connecting to Ollama: {e}"

# ---------------- SESSION STATE ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = {
        "name": "Chat 1",
        "messages": []
    }

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("💬 Chat History")

    # New Chat Button
    if st.button("➕ New Chat"):
        new_chat_id = str(uuid.uuid4())
        chat_number = len(st.session_state.chats) + 1

        st.session_state.chats[new_chat_id] = {
            "name": f"Chat {chat_number}",
            "messages": []
        }

        st.session_state.current_chat = new_chat_id
        st.rerun()

    st.divider()

    # Show all chats
    for chat_id, chat_data in st.session_state.chats.items():
        if st.button(chat_data["name"], key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

# ---------------- MAIN TITLE ----------------
st.title("Simple Chatbot")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    st.success(f"File Uploaded: {uploaded_file.name}")

st.divider()

# ---------------- DISPLAY CURRENT CHAT ----------------
current_chat = st.session_state.chats[st.session_state.current_chat]

for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message here...")

if user_input:

    # Save user message
    current_chat["messages"].append({
        "role": "user",
        "content": user_input
    })

    # Get Ollama response
    bot_reply = ask_ollama(current_chat["messages"])

    # Save assistant message
    current_chat["messages"].append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()
