import zipfile
from xml.etree import ElementTree as ET


def extract_text_odt(file_path):
    """
    Extrai o texto de um arquivo ODT.

    :param file_path: Caminho para o arquivo ODT
    :return: Texto extraído do documento
    """
    try:
        # Abrir o arquivo ODT como um arquivo ZIP
        with zipfile.ZipFile(file_path) as odt_file:
            # Ler o conteúdo do arquivo content.xml
            content = odt_file.read('content.xml')

            # Parsear o XML
            root = ET.fromstring(content)

            # Encontrar todos os elementos de texto
            # Namespace para documentos ODT
            ns = {'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

            # Extrair o texto de todos os elementos <text:p> (parágrafos)
            paragraphs = root.findall('.//text:p', ns)

            # Juntar todos os textos dos parágrafos
            full_text = '\n'.join([p.text for p in paragraphs if p.text])

            return full_text
    except Exception as e:
        print(f"Erro ao extrair texto do arquivo ODT {file_path}: {str(e)}")
        return ""


# Exemplo de uso
if __name__ == "__main__":
    odt_path = "caminho/para/seu/arquivo.odt"
    extracted_text = extract_text_odt(odt_path)
    print(extracted_text)