import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv
from prompt_template import prompt_temp
from file_processing import file_process
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")  
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

os.environ["NVIDIA_API_KEY"] = NVIDIA_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

print(f"  API Keys Loaded")
print(f"  NVIDIA: {NVIDIA_API_KEY[:10]}...")
print(f"  PINECONE: {PINECONE_API_KEY[:10]}...")


pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "indexsample"


if index_name not in pc.list_indexes().names():
    print(f" Index '{index_name}' does not exist.")
    raise ValueError(f"Index '{index_name}' does not exist. Please create it first.")
else:
    print(f" Index '{index_name}' found")




def generate_questions(document_chunk, num_questions=20, words_per_answer=35):
    """Generate questions and answers using RAG"""
    print(f"\n Initializing LLM and Vector Store...")
    
    
    embeddings = NVIDIAEmbeddings()
    
    try:
        print("Creating vector store...")
        vectorstore = PineconeVectorStore.from_documents(
            documents=document_chunk,
            embedding=embeddings,
            index_name=index_name
        )
        print(" Vector store created successfully!")
    except Exception as e:
        print(f" Error creating vector store: {e}")
        print("Loading existing vector store...")
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        print(" Loaded existing vector store")


    llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        temperature=0.2,
        api_key=NVIDIA_API_KEY
    )
    print(" LLM initialized")

    retriever = vectorstore.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 5}
    )
    prompt = prompt_temp()
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "num_questions": lambda x: num_questions, "words_per_answer": lambda x: words_per_answer}
        | prompt
        | llm
        | StrOutputParser()
    )

    print(f"\n Generating {num_questions} questions...")
    try:
        response = rag_chain.invoke(f"Generate {num_questions} questions")
        print("\n" + "="*80)
        print("GENERATED QUESTIONS & ANSWERS")
        print("="*80)
        print(response)
        print("="*80)
        return response
    except Exception as e:
        print(f" Error during generation: {e}")
        return None


def save_output(response, output_file="output.txt"):
    """Save the generated Q&A to a file"""
    if response:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response)
        print(f"\n Output saved to {output_file}")


def main():
   
    filepath = "B:/Users/kiran/Downloads2/SQA_LLM/pdf1.pdf"
    num_questions = 20
    words_per_answer = 35

    print("="*80)
    print("SHORT ANSWER GENERATOR - RAG System")
    print("="*80)
    
    
    document_chunks = file_process(filepath)
    
    
    response = generate_questions(
        document_chunks, 
        num_questions=num_questions,
        words_per_answer=words_per_answer
    )
    

    if response:
        save_output(response, "generated_questions.txt")
        print("\n Process completed successfully!")
    else:
        print("\n  Process failed!")


if __name__ == "__main__":
    main()