import re


def extract_text_md(file_path):
    """
    Extrai o texto de um arquivo Markdown.

    :param file_path: Caminho para o arquivo Markdown
    :return: Texto extraído do documento
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remover links inline
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # Remover imagens
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)

        # Remover códigos inline
        content = re.sub(r'`[^`\n]+`', '', content)

        # Remover blocos de código
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remover cabeçalhos
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)

        # Remover formatação bold e italic
        content = re.sub(r'\*\*?|__?', '', content)

        # Remover listas
        content = re.sub(r'^\s*[-*+]\s', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s', '', content, flags=re.MULTILINE)

        # Remover linhas horizontais
        content = re.sub(r'^\s*[-*_]{3,}\s*$', '', content, flags=re.MULTILINE)

        # Remover espaços em branco extras e linhas vazias
        content = re.sub(r'\n\s*\n', '\n', content)
        content = content.strip()

        return content

    except Exception as e:
        print(f"Erro ao extrair texto do arquivo Markdown {file_path}: {str(e)}")
        return ""


# Exemplo de uso
if __name__ == "__main__":
    md_path = "caminho/para/seu/arquivo.md"
    extracted_text = extract_text_md(md_path)
    print(extracted_text)