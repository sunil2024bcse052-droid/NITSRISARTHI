from langchain_community.document_loaders import WebBaseLoader

urls = [
    "https://nitsri.ac.in/Pages/AboutUs.aspx",
    "https://nitsri.ac.in/Pages/AcademicsAffairs.aspx",
    "https://nitsri.ac.in/Department/Deptindex.aspx?page=a&ItemID=cs&nDeptID=cs",  # CSE dept page
]

loader = WebBaseLoader(urls)
documents = loader.load()

print("Total pages loaded:", len(documents))
for doc in documents:
    print("\n--- Page length:", len(doc.page_content), "characters ---")