import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

START_URL = "https://nitsri.ac.in/"
DOMAIN = "nitsri.ac.in"
MAX_PAGES = 100          # safety limit so it doesn't run forever
DELAY_SECONDS = 1        # be polite to the server, wait 1 sec between requests

visited = set()
to_visit = [START_URL]
found_urls = []
found_pdfs = []


def is_valid_page(url):
    parsed = urlparse(url)
    if DOMAIN not in parsed.netloc:
        return False
    if url.lower().endswith((".jpg", ".png", ".gif", ".jpeg", ".css", ".js")):
        return False
    return True


def crawl():
    while to_visit and len(visited) < MAX_PAGES:
        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            print(f"Failed: {url} ({e})")
            continue

        if response.status_code != 200:
            continue

        content_type = response.headers.get("Content-Type", "")

        if "pdf" in content_type.lower() or url.lower().endswith(".pdf"):
            found_pdfs.append(url)
            print(f"Found PDF: {url}")
            continue

        if "text/html" not in content_type.lower():
            continue

        found_urls.append(url)
        print(f"Crawled ({len(visited)}/{MAX_PAGES}): {url}")

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            full_url = full_url.split("#")[0]  # remove page anchors

            if is_valid_page(full_url) and full_url not in visited and full_url not in to_visit:
                to_visit.append(full_url)

        time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    crawl()

    print(f"\nDone crawling. Total HTML pages found: {len(found_urls)}")
    print(f"Total PDFs found: {len(found_pdfs)}")

    with open("crawled_pages.txt", "w", encoding="utf-8") as f:
        for u in found_urls:
            f.write(u + "\n")

    with open("crawled_pdfs.txt", "w", encoding="utf-8") as f:
        for u in found_pdfs:
            f.write(u + "\n")

    print("\nSaved lists to crawled_pages.txt and crawled_pdfs.txt")