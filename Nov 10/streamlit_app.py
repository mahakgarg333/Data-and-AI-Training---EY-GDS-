import streamlit as st
import requests
from datetime import datetime

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Smart QnA Bot", page_icon="💬", layout="centered")

# ------------------ BACKEND URL ------------------
API_URL = "http://127.0.0.1:8000/ask"  # FastAPI endpoint

# ------------------ CUSTOM STYLES ------------------
st.markdown("""
<style>
body {
    background-color: #f9fafc;
}
.chat-bubble-user {
    background-color: #DCF8C6;
    border-radius: 12px;
    padding: 10px;
    margin: 6px 0;
    max-width: 80%;
    align-self: flex-end;
}
.chat-bubble-bot {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 10px;
    margin: 6px 0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    max-width: 80%;
    align-self: flex-start;
}
.scrollable {
    height: 400px;
    overflow-y: auto;
    display: flex;
    flex-direction: column-reverse;
}
</style>
""", unsafe_allow_html=True)

# ------------------ APP HEADER ------------------
st.title("💬 Smart QnA Bot")
st.caption("Ask me anything — from date and time to text manipulation or general queries!")

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ CHAT DISPLAY ------------------
chat_container = st.container()

with chat_container:
    st.markdown('<div class="scrollable">', unsafe_allow_html=True)
    for msg in reversed(st.session_state.messages):
        role = msg["role"]
        if role == "user":
            st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ INPUT BOX ------------------
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here:", placeholder="e.g., What is the current time?")
    submit = st.form_submit_button("Ask 💭")

# ------------------ HANDLING USER QUERY ------------------
if submit and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(API_URL, json={"question": user_input})
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer received.")
        else:
            answer = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        answer = f"⚠️ Could not connect to backend. ({e})"

    # Display bot response
    st.session_state.messages.append({"role": "bot", "content": answer})

    # Refresh page to show conversation
    st.rerun()

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:gray; font-size:13px;'>"
    f"© {datetime.now().year} Smart QnA Bot | Powered by FastAPI & Streamlit"
    f"</div>", unsafe_allow_html=True)
