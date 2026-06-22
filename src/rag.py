from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "db")


def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3}
    )

    return retriever


if __name__ == "__main__":

    retriever = get_retriever()

    query = "What are the fundamental rights of Indian citizens?"

    docs = retriever.invoke(query)

    print("\n===== RETRIEVED DOCUMENTS =====\n")

    for i, doc in enumerate(docs, start=1):

        print(f"\nDocument {i}")
        print("-" * 50)

        print(doc.page_content[:500])

        print("\nMetadata:")
        print(doc.metadata)
