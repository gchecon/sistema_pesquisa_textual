**Projeto: Sistema de Pesquisa Textual Baseado em LLM Llama3**

---

**Introdução**

O objetivo deste projeto é desenvolver um sistema de pesquisa textual que utilize os modelos de linguagem Llama3. O sistema permitirá a pesquisa em até 50.000 documentos armazenados, provenientes de arquivos PDF, Markdown, ODT ou DOCX. O sistema será utilizado por um único usuário e deverá ser implementado utilizando softwares sem custos de licenciamento. A linguagem de programação preferencial é Python, com possibilidade de módulos em Java, e o banco de dados relacional escolhido é o PostgreSQL.

---

**Arquitetura do Sistema**

1. **Módulo de Processamento em Lote**
   
   - Responsável por ler e processar os documentos.
   - Verifica se os arquivos já foram carregados anteriormente.
   - Extrai o texto dos documentos e gera embeddings vetoriais.
   - Armazena os embeddings em uma base vetorial ou neural.

2. **Módulo de Armazenamento**
   
   - Armazena os embeddings e metadados dos documentos.
   - Utiliza uma base vetorial como FAISS ou Annoy.
   - PostgreSQL para armazenar metadados e referências.

3. **Módulo de Interface de Pesquisa**
   
   - Interface onde o usuário faz perguntas e recebe respostas.
   - Mantém a memória das perguntas anteriores (contexto).
   - Apresenta as referências dos documentos utilizados na resposta.

4. **Módulo LLM Llama3**
   
   - Modelo de linguagem responsável por gerar respostas baseadas nos documentos.

5. **Módulo de Pré-processamento de Documentos**
   
   - Converte documentos nos formatos suportados em texto.
   - Realiza limpeza e normalização dos textos.

---

**Tecnologias Utilizadas**

- **Linguagens de Programação**: Python (principal), Java (módulos opcionais).
- **Modelos de Linguagem**: Llama3 (supondo disponibilidade e licença gratuita).
- **Banco de Dados**: PostgreSQL para metadados; FAISS ou Annoy para armazenamento vetorial.
- **Bibliotecas de Processamento de Documentos**:
  - PDF: PyPDF2, PDFMiner
  - DOCX: python-docx
  - ODT: odfpy
  - Markdown: markdown
- **Bibliotecas de NLP**: NLTK, spaCy, SentenceTransformers
- **Frameworks Web**: Flask ou Django para a interface de usuário

---

**Detalhamento dos Módulos**

1. **Módulo de Processamento em Lote**
   
   - **Funcionalidades**:
     
     - Escanear diretórios em busca de novos arquivos.
     - Verificar duplicatas através de hashes ou timestamps.
     - Extrair texto utilizando bibliotecas específicas.
     - Gerar embeddings dos textos utilizando modelos pré-treinados.
     - Armazenar embeddings e metadados.
   
   - **Implementação**:
     
     - Script em Python agendado via cron ou similar.
     - Uso de multithreading para acelerar o processamento.

2. **Módulo de Armazenamento**
   
   - **Funcionalidades**:
     
     - Armazenar e gerenciar embeddings vetoriais.
     - Permitir busca por similaridade.
     - Armazenar metadados como título, autor, data.
   
   - **Implementação**:
     
     - FAISS para indexação e busca vetorial.
     - PostgreSQL para metadados e controle transacional.

3. **Módulo de Interface de Pesquisa**
   
   - **Funcionalidades**:
     
     - Receber consultas do usuário.
     - Manter contexto das interações anteriores.
     - Exibir respostas e referências aos documentos.
   
   - **Implementação**:
     
     - Aplicação web com Flask ou Django.
     - Interface simples e intuitiva.
     - Gestão de sessões para manter o contexto.

4. **Módulo LLM Llama3**
   
   - **Funcionalidades**:
     
     - Processar consultas do usuário.
     - Gerar respostas baseadas nos documentos mais relevantes.
   
   - **Implementação**:
     
     - Integração do modelo Llama3 via API ou biblioteca.
     - Execução local para evitar custos e dependência de terceiros.

5. **Módulo de Pré-processamento de Documentos**
   
   - **Funcionalidades**:
     
     - Converter documentos em texto bruto.
     - Limpeza e normalização (remoção de stopwords, lematização).
   
   - **Implementação**:
     
     - Utilização de NLTK ou spaCy para NLP.
     - Scripts em Python para processamento em lote.

---

**Fluxo de Operação**

1. **Importação de Documentos**
   
   - O sistema verifica novos arquivos em diretórios pré-definidos.
   - Documentos são processados e textos extraídos.
   - Geração de embeddings e armazenamento.

2. **Processo de Pesquisa**
   
   - O usuário insere uma consulta na interface.
   - O sistema gera um embedding da consulta.
   - Busca os embeddings mais similares na base vetorial.
   - Recupera os documentos relevantes.
   - O Llama3 gera uma resposta baseada nesses documentos.
   - A resposta e as referências são apresentadas ao usuário.

3. **Gestão de Contexto**
   
   - O sistema mantém histórico das interações.
   - Utiliza o contexto para melhorar respostas subsequentes.

---

**Considerações Técnicas**

- **Armazenamento Vetorial**
  
  - **FAISS**: Alta performance para buscas em grandes conjuntos de dados.
  - **Annoy**: Alternativa leve e eficiente.

- **Modelo de Embeddings**
  
  - Utilizar modelos como SentenceTransformers (ex: all-MiniLM-L6-v2).
  - Modelos devem ser de código aberto e gratuitos.

- **Hardware Necessário**
  
  - GPU recomendada para processamento eficiente do Llama3.
  - Espaço em disco suficiente para armazenar embeddings e documentos.

---

**Plano de Desenvolvimento**

1. **Fase de Planejamento**
   
   - Definir requisitos detalhados.
   - Planejar arquitetura e tecnologias específicas.

2. **Desenvolvimento do Módulo de Pré-processamento**
   
   - Implementar extração de texto dos formatos suportados.
   - Testar com diferentes tipos de documentos.

3. **Implementação do Módulo de Processamento em Lote**
   
   - Desenvolver rotina para processamento periódico dos documentos.
   - Implementar verificação de duplicatas.

4. **Configuração do Armazenamento Vetorial e Banco de Dados**
   
   - Instalar e configurar FAISS ou Annoy.
   - Configurar PostgreSQL para metadados.

5. **Integração do Llama3**
   
   - Instalar o modelo Llama3 localmente.
   - Desenvolver interface para interação com o modelo.

6. **Desenvolvimento da Interface de Usuário**
   
   - Criar front-end simples com Flask ou Django.
   - Implementar funcionalidades de busca e exibição de resultados.

7. **Teste e Validação**
   
   - Testar todos os módulos individualmente.
   - Realizar testes de desempenho e carga.

8. **Otimização**
   
   - Melhorar tempos de resposta.
   - Otimizar uso de recursos (CPU, memória).

9. **Documentação e Treinamento**
   
   - Documentar código e processos.
   - Criar manual de usuário.

10. **Implantação**
    
    - Configurar ambiente de produção.
    - Transferir dados e configurar backups.

---

**Considerações Finais**

Este projeto integra várias tecnologias de código aberto para fornecer um sistema de pesquisa robusto e eficiente. Com a utilização do Llama3, espera-se que as respostas sejam contextuais e precisas. A escolha de ferramentas sem custos de licenciamento permite uma solução econômica, sem comprometer a qualidade. A implementação em Python garante facilidade de desenvolvimento e manutenção, enquanto módulos em Java podem ser utilizados quando necessário.

**Próximos Passos**

- Verificar a disponibilidade e requisitos de hardware para o Llama3.
- Avaliar a necessidade de recursos adicionais (como GPUs).
- Iniciar o desenvolvimento seguindo o plano estabelecido.

---

**Nota**: Certifique-se de que todas as ferramentas e modelos utilizados estejam em conformidade com suas licenças de uso. Mantenha-se atualizado com as políticas de uso do Llama3 e outras bibliotecas envolvidas.

-------

**<mark>Desenvolvimento do Módulo de Processamento em Lote no Windows 11</mark>**

---

**Visão Geral**

O módulo de processamento em lote é fundamental para o sistema de pesquisa textual, pois prepara os documentos para serem indexados e pesquisados posteriormente. A implementação no Windows 11 requer algumas adaptações, especialmente em relação ao agendamento de tarefas e uso de variáveis de ambiente.

---

**Módulo de Processamento em Lote**

**1. Configuração do Ambiente**

- **Linguagem de Programação**: Python 3.x

- **Bibliotecas Necessárias**:
  
  - **Processamento de Arquivos**:
    - `PyPDF2` ou `pdfminer.six` para PDFs
    - `python-docx` para DOCX
    - `odfpy` para ODT
    - `markdown` para Markdown
  - **Processamento de Texto**:
    - `sentence_transformers` para geração de embeddings
    - `nltk` ou `spaCy` para pré-processamento (opcional)
  - **Armazenamento**:
    - `faiss` ou `annoy` para índices vetoriais
    - `psycopg2` para conexão com PostgreSQL
  - **Utilitários**:
    - `hashlib` para gerar hashes
    - `os`, `glob`, `pathlib` para manipulação de arquivos e diretórios
    - `concurrent.futures` para multithreading

- **Variáveis de Ambiente**:
  
  | Variável            | Descrição                                             |
  | ------------------- | ----------------------------------------------------- |
  | `DOCUMENTS_PATH`    | Caminho dos diretórios com os documentos              |
  | `PROCESSED_DB_PATH` | Caminho para o banco de dados de arquivos processados |
  | `EMBEDDINGS_PATH`   | Caminho para armazenar os embeddings                  |
  | `THREADS_COUNT`     | Número de threads para processamento paralelo         |
  | `POSTGRESQL_URL`    | URL de conexão com o PostgreSQL (se aplicável)        |

- **Como Definir Variáveis de Ambiente no Windows 11**:
  
  1. Pressione `Win + X` e selecione **Sistema**.
  2. Clique em **Configurações avançadas do sistema**.
  3. Na aba **Avançado**, clique em **Variáveis de Ambiente**.
  4. Em **Variáveis do Sistema** ou **Variáveis de Usuário**, clique em **Novo** e adicione as variáveis necessárias.

---

**2. Implementação do Script em Python**

O script será responsável por escanear os diretórios, processar os arquivos e armazenar os embeddings e metadados.

**2.1. Importações e Configurações Iniciais**

```python
import os
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sqlite3  # Ou psycopg2 para PostgreSQL
from sentence_transformers import SentenceTransformer
import faiss  # Se optar por usar FAISS
# Importar bibliotecas para processamento de cada tipo de arquivo
```

**2.2. Leitura das Variáveis de Ambiente**

```python
DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
PROCESSED_DB_PATH = os.getenv('PROCESSED_DB_PATH', './processed_files.db')
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')
THREADS_COUNT = int(os.getenv('THREADS_COUNT', '4'))
```

**2.3. Configuração do Banco de Dados de Metadados**

Usando SQLite para simplicidade (pode ser substituído por PostgreSQL):

```python
conn = sqlite3.connect(PROCESSED_DB_PATH)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files_processed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        file_hash TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
```

**2.4. Funções para Verificação de Duplicatas**

```python
def calculate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_duplicate(file_path):
    file_hash = calculate_file_hash(file_path)
    cursor.execute('SELECT 1 FROM files_processed WHERE file_hash = ?', (file_hash,))
    return cursor.fetchone() is not None

def update_processed_files(file_path):
    file_hash = calculate_file_hash(file_path)
    cursor.execute('INSERT OR IGNORE INTO files_processed (file_path, file_hash) VALUES (?, ?)', (file_path, file_hash))
    conn.commit()
```

**2.5. Funções para Extração de Texto**

```python
def extract_text(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return extract_text_pdf(file_path)
    elif ext == '.docx':
        return extract_text_docx(file_path)
    elif ext == '.odt':
        return extract_text_odt(file_path)
    elif ext == '.md':
        return extract_text_md(file_path)
    else:
        print(f'Formato não suportado: {ext}')
        return None

# Implementação das funções específicas
def extract_text_pdf(file_path):
    # Implementar extração de texto para PDF
    pass

def extract_text_docx(file_path):
    # Implementar extração de texto para DOCX
    pass

def extract_text_odt(file_path):
    # Implementar extração de texto para ODT
    pass

def extract_text_md(file_path):
    # Implementar extração de texto para Markdown
    pass
```

**2.6. Função para Geração de Embeddings**

```python
# Carregar o modelo uma única vez
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    embedding = model.encode(text)
    return embedding
```

**2.7. Função para Armazenar Embeddings e Metadados**

```python
def store_embedding(file_path, embedding):
    # Exemplo usando FAISS
    dimension = embedding.shape[0]
    if not os.path.exists(EMBEDDINGS_PATH):
        os.makedirs(EMBEDDINGS_PATH)
    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.IndexFlatL2(dimension)

    index.add(embedding.reshape(1, -1))
    faiss.write_index(index, index_path)

    # Atualizar metadados
    update_processed_files(file_path)
```

**2.8. Função Principal de Processamento**

```python
def process_file(file_path):
    try:
        if is_duplicate(file_path):
            print(f'{file_path} já foi processado.')
            return
        text = extract_text(file_path)
        if text:
            embedding = generate_embedding(text)
            store_embedding(file_path, embedding)
            print(f'Arquivo processado: {file_path}')
        else:
            print(f'Não foi possível extrair texto de {file_path}.')
    except Exception as e:
        print(f'Erro ao processar {file_path}: {e}')
```

**2.9. Função para Escanear Diretórios e Processar Arquivos**

```python
def scan_and_process():
    files = []
    for root, dirs, filenames in os.walk(DOCUMENTS_PATH):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    with ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        executor.map(process_file, files)
```

**2.10. Ponto de Entrada do Script**

```python
if __name__ == '__main__':
    scan_and_process()
    conn.close()
```

---

**3. Agendamento do Script no Windows 11**

Como o Windows não possui `cron`, utilizaremos o **Agendador de Tarefas**:

1. **Abrir o Agendador de Tarefas**:
   
   - Pressione `Win + R`, digite `taskschd.msc` e pressione Enter.

2. **Criar uma Nova Tarefa**:
   
   - Clique em **Criar Tarefa** no painel **Ações**.

3. **Configurar a Tarefa**:
   
   - **Geral**:
     - Nomeie a tarefa (por exemplo, "Processamento de Documentos").
     - Marque a opção **Executar com os privilégios mais altos** se necessário.
   - **Triggers**:
     - Adicione um novo gatilho (por exemplo, diariamente, ao logon, a cada hora, etc.).
   - **Ações**:
     - Adicione uma nova ação:
       - **Programa/script**: Caminho completo para o interpretador Python (por exemplo, `C:\Python39\python.exe`).
       - **Adicionar argumentos**: Caminho completo para o script (por exemplo, `C:\meu_projeto\processamento_lote.py`).
   - **Condições e Configurações**:
     - Ajuste conforme necessário (por exemplo, para executar mesmo que o usuário não esteja logado).

4. **Salvar a Tarefa**:
   
   - Clique em **OK** e forneça as credenciais se solicitado.

---

**4. Uso de Variáveis de Ambiente**

As variáveis de ambiente permitem configurar o comportamento do script sem modificar o código:

- **DOCUMENTS_PATH**: Diretório onde os documentos estão armazenados.
- **PROCESSED_DB_PATH**: Caminho para o banco de dados de arquivos processados.
- **EMBEDDINGS_PATH**: Diretório onde os embeddings serão salvos.
- **THREADS_COUNT**: Número de threads para processamento paralelo.

**Definindo Variáveis de Ambiente Temporariamente no Script**:

Você pode criar um arquivo `.env` ou definir as variáveis diretamente no ambiente do sistema.

---

**5. Testes e Validação**

- **Teste com um Conjunto Pequeno de Arquivos**:
  
  - Coloque alguns arquivos de cada formato suportado no diretório especificado.
  - Execute o script manualmente e verifique se os embeddings são gerados e armazenados corretamente.

- **Verifique o Banco de Dados de Metadados**:
  
  - Certifique-se de que os registros estão sendo inseridos e que a verificação de duplicatas funciona.

- **Logs e Mensagens de Erro**:
  
  - Adicione logs mais detalhados se necessário, utilizando a biblioteca `logging` do Python.

---

**6. Integração com Outros Módulos**

- **Módulo de Armazenamento**:
  
  - Certifique-se de que o formato dos embeddings e metadados está compatível com o módulo de pesquisa.
  - Se estiver usando PostgreSQL para metadados, adapte as funções de banco de dados para usar `psycopg2`.

- **Módulo de Pesquisa**:
  
  - Verifique como os embeddings serão recuperados e utilizados nas consultas.

---

**7. Considerações Finais**

- **Licenças**:
  
  - Verifique as licenças das bibliotecas utilizadas para garantir conformidade.

- **Segurança**:
  
  - Proteja informações sensíveis nos documentos e no banco de dados.
  - Implemente controle de acesso se necessário.

- **Desempenho**:
  
  - Monitore o uso de recursos durante o processamento.
  - Otimize o código e considere recursos de hardware adicionais se necessário.

- **Backup e Recuperação**:
  
  - Implemente rotinas de backup para os embeddings e metadados.

---

**Exemplo Completo do Script**

Devido às limitações de espaço e para evitar código excessivamente longo, não podemos fornecer o script completo aqui. No entanto, os trechos de código fornecidos podem ser combinados e ajustados para formar o script completo do módulo de processamento em lote.

---

**Próximos Passos**

- **Implementar Funcionalidades Pendentes**:
  
  - Preencher as funções de extração de texto específicas para cada tipo de arquivo.
  - Implementar tratamento de exceções mais robusto.

- **Testes Extensivos**:
  
  - Realizar testes com um conjunto maior de documentos.
  - Validar o desempenho e ajustar o número de threads se necessário.

- **Documentação**:
  
  - Comentar o código e criar documentação para facilitar a manutenção futura.

- **Integração e Implantação**:
  
  - Integrar com os demais módulos do sistema.
  - Implantar em um ambiente de produção, se aplicável.

---

**Conclusão**

O módulo de processamento em lote é essencial para preparar os documentos para serem pesquisados pelo sistema. Ao adaptá-lo para o Windows 11 e utilizar variáveis de ambiente, garantimos flexibilidade e facilidade de configuração. Com o uso de multithreading, o processamento torna-se mais eficiente, permitindo lidar com um grande número de documentos.

---

**Observação Final**

Lembre-se de que este é um guia para o desenvolvimento do módulo. É importante adaptar e ajustar o código conforme as necessidades específicas do seu projeto e ambiente.
