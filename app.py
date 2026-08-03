import streamlit as st
from chatbot import ask_chatbot

st.set_page_config(
    page_title="NITSriSarthi - College Chatbot",
    page_icon="🎓",
    layout="wide",
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🎓 NITSriSarthi")
    st.caption("Your NIT Srinagar CSE assistant")

    st.markdown("---")

    st.subheader("💡 Try asking:")

    sample_questions = [
        "What are the hostel rules?",
        "Give me the DBMS syllabus",
        "Timetable for 3rd semester section A on Monday",
        "What are the college holidays this year?",
        "Tell me about NIT Srinagar",
    ]

    for q in sample_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Built for NIT Srinagar CSE Department")

# ---------- Main chat area ----------
st.title("🎓 NITSriSarthi College Chatbot")
st.caption("Ask about syllabus, hostel rules, timetable, or general college info")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Show a welcome message if chat is empty
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(
            "👋 Hi! I'm NITSriSarthi, your NIT Srinagar CSE assistant. "
            "Ask me about syllabus, hostel rules, timetable, or anything about the college. "
            "You can also click a sample question in the sidebar to get started."
        )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def handle_question(question):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_chatbot(question)
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# Handle a sample question clicked from the sidebar
if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    handle_question(q)

# Handle a typed question
question = st.chat_input("Ask a question...")
if question:
    handle_question(question)