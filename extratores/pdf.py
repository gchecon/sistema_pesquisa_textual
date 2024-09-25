import io
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import PyPDF2


def extract_text_pdf(file_path):
    # Tenta extrair o texto diretamente do PDF
    text = extract_text_direct(file_path)

    # Se o texto extraído não for significativo, usa OCR
    if not is_text_significant(text):
        text = extract_text_ocr(file_path)

    return text


def extract_text_direct(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def is_text_significant(text):
    # Verifica se o texto extraído é significativo
    # Isso é uma heurística simples e pode precisar ser ajustada
    words = text.split()
    return len(words) > 50 and sum(len(word) > 2 for word in words) / len(words) > 0.5


def extract_text_ocr(file_path):
    text = ""
    images = convert_from_path(file_path)

    for i, image in enumerate(images):
        text += pytesseract.image_to_string(image) + "\n"

    return text


# Exemplo de uso
if __name__ == "__main__":
    pdf_path = "caminho/para/seu/arquivo.pdf"
    extracted_text = extract_text_pdf(pdf_path)
    print(extracted_text)