from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from ingest import load_documents, split_documents


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "data" / "chroma"


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    print("\nLoading banking policy documents...")

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    print("\nSplitting documents into chunks...")

    chunks = split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # --------------------------------------------------
    # EMBEDDING MODEL
    # --------------------------------------------------

    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    # --------------------------------------------------
    # CREATE CHROMA DATABASE
    # --------------------------------------------------

    print("\nCreating ChromaDB...")

    vector_store = Chroma(
        collection_name="banking_policies",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    # --------------------------------------------------
    # ADD DOCUMENTS
    # --------------------------------------------------

    print("\nAdding chunks to ChromaDB...")

    vector_store.add_documents(chunks)

    print(f"Added {len(chunks)} chunks to ChromaDB.")

    print("\nVector store created successfully!")

    print(f"Location: {CHROMA_DIR}")