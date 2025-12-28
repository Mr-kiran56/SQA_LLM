from langchain_text_splitters import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.document import Document


def file_process(file_path):
    """Process PDF file and split into chunks"""
    print(f"\n Processing file: {file_path}")
    
    loader = PyPDFLoader(file_path)
    loader_text = loader.load()
    print(f" Loaded {len(loader_text)} pages")

    text_overall = ""
    for doc in loader_text:
        text_overall += doc.page_content


    textdocs = TokenTextSplitter(chunk_size=10000, chunk_overlap=200)
    texts = textdocs.split_text(text_overall)
    print(f" Created {len(texts)} large chunks")

    
    document = [Document(page_content=t) for t in texts]

    documents_texts = TokenTextSplitter(chunk_size=490, chunk_overlap=400)
    document_chunk = documents_texts.split_documents(document)
    print(f" Created {len(document_chunk)} final chunks")

    return document_chunk
