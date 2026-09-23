from scripts.rag import get_retriever


def test_retrieval():

    question = "What are the KYC requirements?"

    print("=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    print("\nQuestion:")
    print(question)

    retriever = get_retriever()

    documents = retriever.invoke(question)

    print("\n" + "=" * 60)
    print("RETRIEVED DOCUMENTS")
    print("=" * 60)

    print(f"\nTotal documents retrieved: {len(documents)}")

    for index, document in enumerate(documents, start=1):

        print("\n" + "-" * 60)
        print(f"RESULT {index}")

        print(
            "Source:",
            document.metadata.get("source", "Unknown")
        )

        print("\nContent:")
        print(document.page_content[:500])


if __name__ == "__main__":
    test_retrieval()