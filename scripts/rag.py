
import sys
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import BASE_DIR, POLICIES_DIR

# ============================================================
# CONFIGURATION
# ============================================================

ENV_PATH = BASE_DIR / ".env"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_COLLECTION = "banking_policies"
LLM_MODEL = "gemini-3.5-flash-lite"

load_dotenv(ENV_PATH)

FALLBACK_ANSWER = (
    "I couldn't find this information in the available "
    "banking policy documents."
)


# ============================================================
# POLICY DOCUMENTS
# ============================================================

def get_policy_document_list():
    """Return available Markdown policy filenames."""

    if not POLICIES_DIR.exists():
        return []

    return sorted(
        file.name
        for file in POLICIES_DIR.glob("*.md")
    )


# ============================================================
# DOCUMENT LIST DETECTION
# ============================================================

def is_document_list_question(query: str) -> bool:
    query = query.lower().strip()

    document_list_phrases = [
        "what policy files are available",
        "which policy files are available",
        "list available policy files",
        "list all policy documents",
        "show all policy documents",
        "what policy documents are available",
        "which policy documents are available",
        "what documents are available",
        "which documents are available",
        "list available documents",
        "show available documents",
        "what files are available",
        "list all files",
        "show all files",
    ]

    return any(
        phrase in query
        for phrase in document_list_phrases
    )


# ============================================================
# EMBEDDINGS
# ============================================================

@st.cache_resource(show_spinner=False)
def get_embeddings():
    print(
        "\n[DEBUG] Loading embedding model...",
        flush=True
    )

    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print(
        "[DEBUG] Embedding model loaded.",
        flush=True
    )

    return embeddings


# ============================================================
# CHROMA VECTOR STORE
# ============================================================

@st.cache_resource(show_spinner=False)
def get_vector_store():
    print(
        "\n[DEBUG] Loading Chroma vector store...",
        flush=True
    )

    from langchain_chroma import Chroma

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )

    print(
        "[DEBUG] Chroma vector store loaded.",
        flush=True
    )

    return vector_store


# ============================================================
# DOCUMENT ROUTING
# ============================================================

def get_retriever(query: str):
    print(
        "\n[DEBUG] Entered get_retriever().",
        flush=True
    )

    vector_store = get_vector_store()
    query_lower = query.lower()

    matched_sources = []

    # KYC
    if "kyc" in query_lower:
        matched_sources = [
            "kyc_requirements.md"
        ]

    # PERSONAL LOAN
    elif (
        "personal loan" in query_lower
        or "personal-loan" in query_lower
    ):
        matched_sources = [
            "personal_loan_policy.md"
        ]

    # GENERAL LOAN
    elif (
        "loan" in query_lower
        or "borrowing" in query_lower
    ):
        matched_sources = [
            "loan_faq.md",
            "personal_loan_policy.md",
        ]

    # SAVINGS ACCOUNT
    elif (
        "savings account" in query_lower
        or "saving account" in query_lower
    ):
        matched_sources = [
            "savings_account_policy.md"
        ]

    # CURRENT ACCOUNT
    elif "current account" in query_lower:
        matched_sources = [
            "current_account_policy.md"
        ]

    # ATM
    elif "atm" in query_lower:
        matched_sources = [
            "atm_policy.md"
        ]

    # DEBIT CARD
    elif "debit card" in query_lower:
        matched_sources = [
            "debit_card_guide.md"
        ]

    # CREDIT CARD
    elif "credit card" in query_lower:
        matched_sources = [
            "credit_card_guide.md"
        ]

    # DIGITAL BANKING
    elif "digital banking" in query_lower:
        matched_sources = [
            "digital_banking_guide.md"
        ]

    # MOBILE BANKING
    elif "mobile banking" in query_lower:
        matched_sources = [
            "mobile_banking_guide.md"
        ]

    # NEFT / RTGS / IMPS
    elif any(
        keyword in query_lower
        for keyword in ["neft", "rtgs", "imps"]
    ):
        matched_sources = [
            "neft_rtgs_imps_guide.md"
        ]

    # FUND TRANSFER
    elif any(
        phrase in query_lower
        for phrase in [
            "fund transfer",
            "transfer money",
            "money transfer",
        ]
    ):
        matched_sources = [
            "fund_transfer_guide.md"
        ]

    # FRAUD / SECURITY
    elif any(
        keyword in query_lower
        for keyword in [
            "fraud",
            "scam",
            "security",
            "unauthorized transaction",
            "unauthorised transaction",
        ]
    ):
        matched_sources = [
            "fraud_and_security_guide.md"
        ]

    # ACCOUNT CLOSURE
    elif any(
        phrase in query_lower
        for phrase in [
            "close account",
            "account closure",
            "closing account",
        ]
    ):
        matched_sources = [
            "account_closure_policy.md"
        ]

    # FEES
    elif any(
        keyword in query_lower
        for keyword in [
            "fee",
            "fees",
            "charge",
            "charges",
        ]
    ):
        matched_sources = [
            "fees_and_charges.md"
        ]

    # CUSTOMER SUPPORT
    elif any(
        phrase in query_lower
        for phrase in [
            "customer support",
            "customer service",
            "contact support",
        ]
    ):
        matched_sources = [
            "customer_support_policy.md"
        ]

    # COMPLAINT
    elif any(
        keyword in query_lower
        for keyword in [
            "complaint",
            "grievance",
        ]
    ):
        matched_sources = [
            "complaint_resolution_policy.md"
        ]

    # BRANCH
    elif "branch" in query_lower:
        matched_sources = [
            "branch_banking_faq.md"
        ]

    print(
        f"[DEBUG] Matched policy files: {matched_sources}",
        flush=True
    )

    # ROUTED SEARCH
    if matched_sources:
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 8,
                "filter": {
                    "source": {
                        "$in": matched_sources
                    }
                },
            }
        )

        return retriever, matched_sources

    # GENERAL SIMILARITY SEARCH
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 6
        }
    )

    return retriever, []


# ============================================================
# GEMINI
# ============================================================

@st.cache_resource(show_spinner=False)
def get_llm():
    print(
        "\n[DEBUG] Initializing Gemini...",
        flush=True
    )

    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL
    )

    print(
        "[DEBUG] Gemini initialized.",
        flush=True
    )

    return llm


# ============================================================
# EXTRACT RESPONSE TEXT
# ============================================================

def extract_response_text(response):
    if response is None:
        return ""

    if isinstance(response, str):
        return response

    content = getattr(
        response,
        "content",
        None
    )

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):
                if "text" in item:
                    text_parts.append(
                        str(item["text"])
                    )

        return "\n".join(text_parts)

    return str(response)


# ============================================================
# MAIN RAG FUNCTION
# ============================================================

def ask_banking_assistant(question: str):

    # VALIDATE QUESTION
    if not question or not question.strip():
        return (
            "Please enter a banking question.",
            [],
            [],
        )

    question = question.strip()

    print(
        "\n[DEBUG 0] Question received.",
        flush=True
    )

    # ONLY LIST FILES WHEN EXPLICITLY ASKED
    if is_document_list_question(question):
        documents = get_policy_document_list()

        answer = (
            "The available banking policy documents are:\n\n"
            + "\n".join(
                f"- {document}"
                for document in documents
            )
        )

        return (
            answer,
            documents,
            documents,
        )

    # RETRIEVE RELEVANT DOCUMENTS
    retrieval_start = time.time()

    try:
        print(
            "\n[DEBUG 1] Starting retrieval...",
            flush=True
        )

        print(
            "[DEBUG 2] Loading retriever...",
            flush=True
        )

        retriever, routed_sources = get_retriever(
            question
        )

        print(
            "[DEBUG 3] Retriever ready.",
            flush=True
        )

        print(
            "[DEBUG 4] Searching Chroma...",
            flush=True
        )

        documents = retriever.invoke(
            question
        )

        print(
            f"[DEBUG 5] Retrieved {len(documents)} documents.",
            flush=True
        )

    except Exception as error:
        print(
            "\n[RAG RETRIEVAL ERROR]",
            flush=True
        )

        print(
            repr(error),
            flush=True
        )

        return (
            "I couldn't retrieve the relevant banking policy information.",
            [],
            [],
        )

    retrieval_time = time.time() - retrieval_start

    print(
        f"\n[RAG TIMING] Retrieval: "
        f"{retrieval_time:.2f} seconds",
        flush=True
    )

    # NO RETRIEVED DOCUMENTS
    if not documents:
        return (
            FALLBACK_ANSWER,
            [],
            [],
        )

    # BUILD CONTEXT
    context_parts = []
    sources = []

    for document in documents:
        content = document.page_content
        metadata = document.metadata or {}

        source = metadata.get(
            "source",
            "Unknown source"
        )

        source_name = Path(
            str(source)
        ).name

        if source_name not in sources:
            sources.append(source_name)

        context_parts.append(
            f"""
SOURCE: {source_name}

CONTENT:
{content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    print(
        "[DEBUG 6] Context built.",
        flush=True
    )

    # GROUNDED PROMPT
    prompt = f"""
You are a banking policy assistant.

Answer the user's question using ONLY the
banking policy context provided below.

Do not use outside knowledge.
Do not invent banking rules, requirements, limits,
fees, ages, or eligibility criteria.

The user may ask more than one thing.
Answer every part that is supported by the context.

If the user provides an age, amount, loan type,
or other condition, consider it when answering.

For questions about required documents:
- List only documents explicitly mentioned in the context.
- Do not assume that general KYC documents are required
  for a specific loan unless the policy says so.
- If the context does not provide the answer,
  clearly say that the information was not found.

For eligibility questions:
- State the criteria only if the policy provides them.
- Do not assume that someone is eligible based only on age.

Do not mix unrelated policies.
Keep the answer simple, clear, and direct.
Use bullet points for lists.

If the answer is not present in the context,
respond exactly with:

"{FALLBACK_ANSWER}"

USER QUESTION:
{question}

BANKING POLICY CONTEXT:
{context}
"""

    # GENERATE ANSWER
    llm_start = time.time()

    try:
        print(
            "\n[DEBUG 7] Getting Gemini model...",
            flush=True
        )

        llm = get_llm()

        print(
            "[DEBUG 8] Sending prompt to Gemini...",
            flush=True
        )

        response = llm.invoke(
            prompt
        )

        print(
            "[DEBUG 9] Gemini response received.",
            flush=True
        )

        answer = extract_response_text(
            response
        )

    except Exception as error:
        print(
            "\n[RAG LLM ERROR]",
            flush=True
        )

        print(
            repr(error),
            flush=True
        )

        return (
            "Something went wrong while generating the answer. Please try again.",
            sources,
            [],
        )

    llm_time = time.time() - llm_start

    print(
        f"[RAG TIMING] LLM response: "
        f"{llm_time:.2f} seconds",
        flush=True
    )

    print(
        f"[RAG TIMING] Total: "
        f"{retrieval_time + llm_time:.2f} seconds",
        flush=True
    )

    # EMPTY RESPONSE HANDLING
    if not answer or not answer.strip():
        answer = FALLBACK_ANSWER

    # RETURN
    # Home.py should not display sources.
    return (
        answer.strip(),
        sources,
        [],
    )


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    print("\n================================")
    print("BANKING ASSISTANT TEST")
    print("================================")

    question = input(
        "\nAsk a banking question: "
    )

    answer, sources, _ = ask_banking_assistant(
        question
    )

    print("\n-------------------------------")
    print("ANSWER")
    print("-------------------------------")

    print(answer)

    print("\n-------------------------------")
    print("SOURCES (terminal only)")
    print("-------------------------------")

    for source in sources:
        print("-", source)