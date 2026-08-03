# NITSRISARTHI 🎓

**A hybrid AI chatbot for NIT Srinagar CSE Department** — combining document-based Q&A (RAG) with structured database lookups, built as a college project.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20API-orange)

---

## 📌 Overview

NITSRISARTHI answers two kinds of questions:
- **Unstructured questions** — syllabus, hostel rules, college info — answered using Retrieval-Augmented Generation (RAG) over documents and the official college website
- **Structured questions** — timetable lookups — answered using direct, exact database queries

This hybrid approach means factual, tabular data (like class timings) is always accurate, while general knowledge questions get natural, context-grounded answers from an LLM.

---

## ✨ Features

- 📄 Answers questions from syllabus PDFs, hostel rules, and scanned document images (via OCR)
- 🌐 Automatically crawls and ingests content from the official NIT Srinagar website, including linked PDFs
- 🗓️ Structured timetable lookup by semester, section, and day
- 💬 Clarifying follow-up questions when a request is ambiguous (e.g. asks for semester/section instead of guessing)
- 🛡️ Graceful error handling — API failures or missing data won't crash the app
- ⚡ Cached database connections for faster responses
- 🧹 Deduplication logic to keep the knowledge base clean and relevant

---

## 🏗️ Architecture

| Component | Technology |
|---|---|
| Web interface | Streamlit |
| LLM (answer generation) | Groq API (llama-3.3-70b-versatile) |
| Vector database (RAG) | ChromaDB |
| Embeddings | sentence-transformers |
| Structured data storage | SQLite |
| PDF text extraction | pypdf |
| OCR (image text extraction) | pytesseract (Tesseract OCR) |
| Web scraping/crawling | requests + BeautifulSoup |
| Document chunking | langchain-text-splitters |

---

## ⚙️ How It Works

1. **Document ingestion** — PDFs and images are OCR'd (if needed), chunked, and embedded into ChromaDB via `reg_embed.py`
2. **Website ingestion** — `crawl_site.py` automatically discovers all internal pages and linked PDFs on the NIT Srinagar website; `web_embed.py` and `pdf_embed_from_urls.py` embed this content, filtering out duplicate navigation/menu text
3. **Structured data** — Timetable data is parsed and stored in SQLite (`college_data.db`) via `build_timetable_db.py`
4. **Query routing** — `chatbot.py` detects timetable-related questions via keywords. If details are missing, it asks for clarification. Otherwise, it retrieves relevant chunks from ChromaDB and generates a grounded answer using the Groq LLM
5. **Interface** — `app.py` provides a Streamlit chat interface for users

---

## 📂 Project Structure
