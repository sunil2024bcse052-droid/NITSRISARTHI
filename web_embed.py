from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "college_docs"

# List of NIT Srinagar pages to pull data from
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


def add_to_chromadb(chunks, source_name):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    existing_count = collection.count()

    ids = [f"web_{source_name}_{i}_{existing_count}" for i in range(len(chunks))]
    metadatas = [{"source": source_name} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas,
    )


def main():
    print(f"Loading {len(URLS)} web pages...")
    documents = load_web_pages(URLS)
    print(f"Loaded {len(documents)} pages successfully.")

    total_chunks_added = 0

    for doc in documents:
        source_url = doc.metadata.get("source", "unknown")
        text = doc.page_content

        if not text.strip():
            print(f"Skipping empty page: {source_url}")
            continue

        chunks = chunk_text(text)
        add_to_chromadb(chunks, source_name=source_url)

        print(f"Added {len(chunks)} chunks from: {source_url}")
        total_chunks_added += len(chunks)

    print(f"\nDone. Total new chunks added: {total_chunks_added}")


if __name__ == "__main__":
    main()