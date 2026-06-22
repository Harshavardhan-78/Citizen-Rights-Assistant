# src/ingest.py

# Load markdown files from the data folder
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)

# Split large documents into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Convert text chunks into embeddings (vectors)
from langchain_huggingface import HuggingFaceEmbeddings

# Store embeddings inside Chroma Vector DB
from langchain_community.vectorstores import Chroma


# Folder containing legal documents
DATA_PATH = "data"

# Folder where vector database will be stored
DB_PATH = "db"


def load_documents():
    """
    Loads all markdown files from the data folder.
    Returns a list of Document objects.
    """

    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.md",
        loader_cls=TextLoader
    )

    documents = loader.load()

    # Add custom metadata
    for doc in documents:

        source = doc.metadata["source"]

        # Categorize documents
        if "constitution" in source.lower():
            doc.metadata["category"] = "constitution"

        elif "ipc" in source.lower():
            doc.metadata["category"] = "ipc"

        else:
            doc.metadata["category"] = "general"

    return documents


def create_chunks(documents):
    """
    Splits large documents into smaller chunks.
    Overlap helps preserve context between chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks


def create_vector_db(chunks):
    """
    Converts chunks into embeddings and stores them in ChromaDB.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    print("✅ Vector Database Created Successfully")


if __name__ == "__main__":

    # Step 1: Load markdown files
    documents = load_documents()

    print(f"\n📄 Documents Loaded: {len(documents)}")

    # Preview first document
    print("\n===== SAMPLE DOCUMENT =====")
    print(documents[0])

    # Step 2: Chunk documents
    chunks = create_chunks(documents)

    print(f"\n✂️ Chunks Created: {len(chunks)}")

    # Preview first chunk
    print("\n===== SAMPLE CHUNK =====")
    print(chunks[0])

    # Step 3: Create vector database
    create_vector_db(chunks)