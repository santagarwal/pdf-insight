# PDF QA Pipeline (Script Version)
import os
import glob
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

PDF_DIR = "pdfs"
COLLECTION_NAME = "pdf_qa_collection"


def read_pdfs(pdf_dir):
    docs = []
    for pdf_path in glob.glob(os.path.join(pdf_dir, "*.pdf")):
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        docs.append({"filename": os.path.basename(pdf_path), "text": text})
    return docs


def chunk_documents(docs, chunk_size=800, chunk_overlap=50):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["text"]):
            chunks.append({"filename": doc["filename"], "text": chunk})
    return chunks


def embed_and_store(chunks):
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"filename": chunk["filename"]} for chunk in chunks]
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Milvus.from_texts(
        texts,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        metadatas=metadatas,
    )
    return vectorstore


def get_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    return qa


def ask_question(question, qa_chain):
    return qa_chain.run(question)


def main():
    print("Reading PDFs...")
    docs = read_pdfs(PDF_DIR)
    print(f"Loaded {len(docs)} PDFs.")
    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Generated {len(chunks)} chunks.")
    print("Generating embeddings and storing in Milvus...")
    vectorstore = embed_and_store(chunks)
    print("Ready for questions!")
    qa_chain = get_qa_chain(vectorstore)
    while True:
        question = input("Ask a question (or 'exit'): ")
        if question.lower() == "exit":
            break
        answer = ask_question(question, qa_chain)
        print(f"Answer: {answer}\n")


if __name__ == "__main__":
    main()
