# utils.py
import re
from pdfminer.high_level import extract_text
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes a PDF file as raw bytes and returns the text inside it as a string.
    """
    pdf_file = BytesIO(file_bytes)
    text = extract_text(pdf_file)
    return text


def clean_text(text: str) -> str:
    """
    Takes raw messy text and returns clean, normalized text.
    """
    # convert everything to lowercase
    text = text.lower()

    # replace newlines and tabs with a single space
    text = text.replace("\n", " ").replace("\t", " ")

    # remove special characters — keep only letters, numbers, spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # remove leading and trailing spaces
    text = text.strip()

    return text