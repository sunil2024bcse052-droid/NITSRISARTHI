from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"


def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


URLS = load_urls_from_file("crawled_pages.txt")


def load_web_pages(urls):
    loader = WebBaseLoader(urls)
    documents = loader.load()
    return documents


def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def add_to_chromadb(chunks_with_sources, seen_chunks):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    existing_count = collection.count()

    final_chunks = []
    final_sources = []

    for chunk, source in chunks_with_sources:
        stripped = chunk.strip()

        if len(stripped) < 100:
            continue  # too short, likely junk

        if stripped in seen_chunks:
            continue  # duplicate of something already added

        seen_chunks.add(stripped)
        final_chunks.append(chunk)
        final_sources.append(source)

    if not final_chunks:
        return 0

    ids = [f"web_{i}_{existing_count}" for i in range(len(final_chunks))]
    metadatas = [{"source": s} for s in final_sources]

    collection.add(
        documents=final_chunks,
        ids=ids,
        metadatas=metadatas,
    )

    return len(final_chunks)


def main():
    print(f"Loading {len(URLS)} web pages...")
    documents = load_web_pages(URLS)
    print(f"Loaded {len(documents)} pages successfully.")

    seen_chunks = set()
    all_chunks_with_sources = []

    for doc in documents:
        source_url = doc.metadata.get("source", "unknown")
        text = doc.page_content

        if not text.strip():
            continue

        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks_with_sources.append((chunk, source_url))

    print(f"\nTotal raw chunks before dedup: {len(all_chunks_with_sources)}")

    added_count = add_to_chromadb(all_chunks_with_sources, seen_chunks)

    print(f"Total unique chunks added: {added_count}")
    print(f"Duplicates/junk skipped: {len(all_chunks_with_sources) - added_count}")


if __name__ == "__main__":
    main()