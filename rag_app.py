from __future__ import annotations

import argparse
import re
from pathlib import Path
import os
from typing import List

import pytesseract
from PIL import Image
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

TEXT_EXTENSIONS = {".txt", ".md", ".rtf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif", ".webp"}

# Configure tesseract executable path on Windows if present at the default location
# Change this path if your Tesseract installation is located elsewhere.
_TESSERACT_DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if Path(_TESSERACT_DEFAULT).exists():
    pytesseract.pytesseract.tesseract_cmd = _TESSERACT_DEFAULT


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


def build_index(paths: List[Path]) -> List[dict[str, str]]:
    chunks: List[dict[str, str]] = []
    for path in paths:
        text = extract_text_from_path(path)
        if not text.strip():
            continue
        for chunk in split_text(text):
            chunks.append({"source": str(path), "text": chunk})
    return chunks


def normalize(text: str) -> List[str]:
    return re.sub(r"\W+", " ", text.lower()).split()


def search(query: str, chunks: List[dict[str, str]], top_k: int = 3) -> List[tuple[int, dict[str, str]]]:
    query_terms = set(normalize(query))
    scored: List[tuple[int, dict[str, str]]] = []
    for chunk in chunks:
        chunk_terms = set(normalize(chunk["text"]))
        score = sum(1 for term in query_terms if term in chunk_terms)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[:top_k]


def collect_files(paths: List[str]) -> List[Path]:
    collected: List[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            collected.extend(sorted(path.rglob("*")))
        else:
            collected.append(path)
    return [path for path in collected if path.is_file()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple RAG-style search over text, PDF, or image files")
    parser.add_argument("--query", required=True, help="Question or search phrase")
    parser.add_argument("--input", nargs="+", default=["sample_documents"], help="Files or folders to search")
    args = parser.parse_args()

    files = collect_files(args.input)
    if not files:
        raise SystemExit("No searchable files were found.")

    chunks = build_index(files)
    if not chunks:
        raise SystemExit("No text could be extracted from the provided files.")

    results = search(args.query, chunks)
    if not results:
        print("No relevant matches found.")
        return

    print(f"Found {len(results)} match(es):")
    for score, chunk in results:
        print(f"\n[score={score}] {chunk['source']}")
        print(chunk["text"][:500])


if __name__ == "__main__":
    main()
