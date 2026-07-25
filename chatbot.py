import os
from dotenv import load_dotenv
from groq import Groq
import chromadb

load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"


def search_documents(query, top_k=3):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    results = collection.query(query_texts=[query], n_results=top_k)
    documents = results.get("documents", [[]])[0]
    return documents


def ask_chatbot(question):
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

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("College Chatbot (type 'exit' to quit)")
    while True:
        question = input("\nYou: ")
        if question.lower() == "exit":
            break
        answer = ask_chatbot(question)
        print(f"\nBot: {answer}")