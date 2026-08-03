import os
import requests
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from io import BytesIO

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"


def load_pdf_urls(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def extract_text_from_pdf_url(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to download: {url} ({e})")
        return ""

    try:
        reader = PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Failed to read PDF content: {url} ({e})")
        return ""


def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def add_to_chromadb(chunks, source_name):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    existing_count = collection.count()

    ids = [f"pdf_{os.path.basename(source_name)}_{i}_{existing_count}" for i in range(len(chunks))]
    metadatas = [{"source": source_name} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas,
    )


def main():
    pdf_urls = load_pdf_urls("crawled_pdfs.txt")
    print(f"Found {len(pdf_urls)} PDF URLs to process.")

    total_chunks_added = 0

    for url in pdf_urls:
        print(f"\nProcessing: {url}")
        text = extract_text_from_pdf_url(url)

        if not text.strip():
            print(f"Skipping (no text extracted): {url}")
            continue

        chunks = chunk_text(text)
        add_to_chromadb(chunks, source_name=url)

        print(f"Added {len(chunks)} chunks from: {url}")
        total_chunks_added += len(chunks)

    print(f"\nDone. Total new chunks added: {total_chunks_added}")


if __name__ == "__main__":
    main()