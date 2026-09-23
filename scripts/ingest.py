from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

POLICIES_DIR = BASE_DIR / "data" / "policies"


# --------------------------------------------------
# LOAD DOCUMENTS
# --------------------------------------------------

def load_documents():
    documents = []

    for file_path in POLICIES_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "file_path": str(file_path),
            },
        )

        documents.append(document)

    return documents


# --------------------------------------------------
# SPLIT DOCUMENTS
# --------------------------------------------------

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


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

    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\n--- Chunk {i} ---")

        print("Source:", chunk.metadata["source"])

        print("Content:")
        print(chunk.page_content[:500])

        print("-" * 60)