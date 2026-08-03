from chatbot import ask_chatbot

# Test questions grouped by category
TEST_QUESTIONS = {
    "Document-based (RAG)": [
        "What are the hostel rules?",
        "Give me the DBMS syllabus",
        "Tell me about NIT Srinagar",
        "What are the college holidays this year?",
    ],
    "Structured (Timetable)": [
        "What is my timetable for 3rd semester section A on Monday?",
        "What is my timetable",  # missing details, should ask for clarification
        "Timetable for 5th semester section A",  # missing day, should still work
    ],
    "Edge cases": [
        "What is the capital of France?",       # unrelated question
        "asdkjaslkdj",                          # gibberish
        "",                                     # empty input
        "tell me about the college",            # vague/broad
    ],
}


def run_tests():
    for category, questions in TEST_QUESTIONS.items():
        print(f"\n{'='*60}")
        print(f"CATEGORY: {category}")
        print(f"{'='*60}")

        for question in questions:
            print(f"\nQ: {question if question else '(empty input)'}")
            try:
                answer = ask_chatbot(question)
                print(f"A: {answer}")
            except Exception as e:
                print(f"ERROR: {e}")


if __name__ == "__main__":
    run_tests()