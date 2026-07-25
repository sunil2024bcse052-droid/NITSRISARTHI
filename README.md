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

## Tesseract OCR

On Windows, install Tesseract using one of these methods:

- `winget install --id Tesseract.Tesseract -e`
- Download and install the official Windows installer from the Tesseract OCR releases page: https://github.com/tesseract-ocr/tesseract/releases

After installation, verify it by running:

- `tesseract --version`

If `tesseract` is not on PATH, make sure it is installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`, or update the `_TESSERACT_DEFAULT` path in `rag_app.py`.

Then run the app:

- `python rag_app.py --query "your question" --input sample_documents`
