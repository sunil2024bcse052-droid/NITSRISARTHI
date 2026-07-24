# RAG Starter Project

This workspace now contains a small Python-based starter project for searching text from:

- plain text files
- PDF files
- image files (OCR via Tesseract)

## Setup

1. Activate the virtual environment:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `python -m pip install -r requirements.txt`
3. Run the app:
   - `python rag_app.py --query "your question" --input sample_documents`

## Notes

For image OCR, a Tesseract installation is required on the system.
