import os
import re
from dotenv import load_dotenv
from groq import Groq
import chromadb

from timetable_lookup import get_timetable, format_timetable_results

load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"

TIMETABLE_KEYWORDS = ["timetable", "time table", "schedule", "class timing", "hour", "period"]

# Cache the ChromaDB client/collection so we don't reconnect on every question
_chroma_client = None
_chroma_collection = None


def get_collection():
    global _chroma_client, _chroma_collection
    if _chroma_collection is None:
        _chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        _chroma_collection = _chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    return _chroma_collection


def is_timetable_question(question):
    q = question.lower()
    return any(keyword in q for keyword in TIMETABLE_KEYWORDS)


def extract_timetable_filters(question):
    q = question.lower()

    semester = None
    for sem in ["1st", "3rd", "5th", "7th"]:
        if sem in q:
            semester = sem
            break
    if "m.tech" in q or "mtech" in q:
        if "1st" in q:
            semester = "1st M.Tech"
        elif "3rd" in q:
            semester = "3rd M.Tech"

    section = None
    match = re.search(r"section\s*([ab])|sec\s*([ab])", q)
    if match:
        section = (match.group(1) or match.group(2)).upper()

    day = None
    for d in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        if d in q:
            day = d.capitalize()
            break

    return semester, section, day


def search_documents(query, top_k=8):
    try:
        collection = get_collection()
        results = collection.query(query_texts=[query], n_results=top_k)
        documents = results.get("documents", [[]])[0]
        return documents
    except Exception as e:
        print(f"ChromaDB search error: {e}")
        return []


def ask_document_question(question):
    matched_chunks = search_documents(question)

    if not matched_chunks:
        return "I don't have information about that in my current data."

    context = "\n\n".join(matched_chunks)

    prompt = f"""You are a helpful college assistant chatbot.
Use ONLY the following context to answer the question.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:"""

    try:
        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            timeout=15,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API error: {e}")
        return "Sorry, I'm having trouble generating an answer right now. Please try again in a moment."


def ask_chatbot(question):
    if not question or not question.strip():
        return "Please type a question so I can help you."

    if is_timetable_question(question):
        semester, section, day = extract_timetable_filters(question)

        missing = []
        if not semester:
            missing.append("semester (e.g. 3rd, 5th, 7th)")
        if not section:
            missing.append("section (A or B)")

        if missing:
            return (
                "Please tell me your " + " and ".join(missing) +
                " so I can find the right timetable. "
                "Example: 'timetable for 3rd semester section A on Monday'"
            )

        rows = get_timetable(semester=semester, section=section, day=day)

        if not rows:
            return (
                "I couldn't find a matching timetable entry for that semester, section, "
                "and day. Please double check the details and try again."
            )

        return format_timetable_results(rows)

    return ask_document_question(question)


if __name__ == "__main__":
    print("College Hybrid Chatbot (type 'exit' to quit)")
    while True:
        question = input("\nYou: ")
        if question.lower() == "exit":
            break
        answer = ask_chatbot(question)
        print(f"\nBot: {answer}")