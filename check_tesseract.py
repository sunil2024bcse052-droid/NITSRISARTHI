from pathlib import Path
import shutil
import pytesseract

DEFAULT_TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

if __name__ == "__main__":
    path_in_path = shutil.which("tesseract")
    default_exists = DEFAULT_TESSERACT_PATH.exists()

    print("Tesseract PATH check:")
    if path_in_path:
        print(f"  found on PATH: {path_in_path}")
    else:
        print("  not found on PATH")

    print("Default install location check:")
    if default_exists:
        print(f"  found at default path: {DEFAULT_TESSERACT_PATH}")
    else:
        print(f"  not found at default path: {DEFAULT_TESSERACT_PATH}")

    if not path_in_path and not default_exists:
        print("\nTesseract is not installed or not available to this Python environment.")
        print("Install Tesseract on Windows and ensure either:")
        print("  - tesseract is on PATH, or")
        print("  - update the default path in rag_app.py")
    else:
        print("\nTesseract appears to be available.")
        if not path_in_path and default_exists:
            pytesseract.pytesseract.tesseract_cmd = str(DEFAULT_TESSERACT_PATH)
            print("  Using default install path for pytesseract.")
