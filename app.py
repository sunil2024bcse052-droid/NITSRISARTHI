import streamlit as st
from chatbot import ask_chatbot

st.set_page_config(page_title="NITSriSarthi - College Chatbot", page_icon="🎓")

st.title("🎓 NITSriSarthi College Chatbot")
st.caption("Ask about syllabus, hostel rules, or timetable")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_chatbot(question)
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})