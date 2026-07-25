from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import chromadb
import pytesseract
from PIL import Image
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

TEXT_EXTENSIONS = {".txt", ".md", ".rtf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif", ".webp"}

_TESSERACT_DEFAULT = r"C:\Users\asus\OneDrive\Desktop\nitsrisarthi-rag\tesseract.exe"
if Path(_TESSERACT_DEFAULT).exists():
    pytesseract.pytesseract.tesseract_cmd = _TESSERACT_DEFAULT

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"


def extract_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_image(path: Path) -> str:
    with Image.open(path) as image:
        return pytesseract.image_to_string(image)


def extract_text_from_path(path: Path) -> str:
    extension = path.suffix.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(path)
    if extension in IMAGE_EXTENSIONS:
        return extract_text_from_image(path)
    if extension in TEXT_EXTENSIONS:
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {path}")


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def collect_files(paths: List[str]) -> List[Path]:
    collected: List[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            collected.extend(sorted(path.rglob("*")))
        else:
            collected.append(path)
    return [
        p for p in collected
        if p.is_file() and p.suffix.lower() in (TEXT_EXTENSIONS | IMAGE_EXTENSIONS | {".pdf"})
    ]


def build_and_store(paths: List[str]) -> int:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    files = collect_files(paths)
    if not files:
        print("No searchable files found in the given input paths.")
        return 0

    all_chunks: List[str] = []
    all_ids: List[str] = []
    all_metadatas: List[dict] = []

    for path in files:
        print(f"Processing: {path}")
        try:
            text = extract_text_from_path(path)
        except Exception as exc:
            print(f"  Skipped (error): {exc}")
            continue

        if not text.strip():
            print("  Skipped (no text extracted)")
            continue

        chunks = split_text(text)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{path.name}_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadatas.append({"source": str(path)})

    if not all_chunks:
        print("No text could be extracted from any file.")
        return 0

    batch_size = 32
    for i in range(0, len(all_chunks), batch_size):
        collection.upsert(
            documents=all_chunks[i:i + batch_size],
            ids=all_ids[i:i + batch_size],
            metadatas=all_metadatas[i:i + batch_size],
        )

    print(f"\nStored {len(all_chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'.")
    return len(all_chunks)


def query_index(query: str, top_k: int = 3) -> None:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    results = collection.query(query_texts=[query], n_results=top_k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        print("No relevant matches found.")
        return

    print(f"Found {len(documents)} match(es):")
    for doc, meta, dist in zip(documents, metadatas, distances):
        print(f"\n[similarity distance={dist:.4f}] {meta.get('source')}")
        print(doc[:500])


def main() -> None:
    parser = argparse.ArgumentParser(description="Embedding-based RAG search using ChromaDB")
    parser.add_argument("--build", nargs="+", help="Files or folders to ingest")
    parser.add_argument("--query", help="Question or search phrase")
    parser.add_argument("--top_k", type=int, default=3, help="Number of results to return")
    args = parser.parse_args()

    if args.build:
        build_and_store(args.build)

    if args.query:
        query_index(args.query, top_k=args.top_k)

    if not args.build and not args.query:
        print("Provide --build <paths> to ingest files, and/or --query <text> to search.")


if __name__ == "__main__":
    main()