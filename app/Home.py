import streamlit as st
import sys
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.rag import ask_banking_assistant


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏦 Banking Assistant")
st.caption("Ask questions about banking policies, accounts, cards, loans, KYC and more.")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("💬 Banking Assistant")

    st.write(
        "Ask questions about the available banking policies "
        "and get answers based only on the provided documents."
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.messages:

    with st.chat_message("assistant"):
        st.markdown(
            """
            👋 **Hello! I'm your Banking Assistant.**

            You can ask me about:

            - KYC requirements
            - Savings accounts
            - Current accounts
            - Loans
            - Debit & credit cards
            - ATM services
            - NEFT / RTGS / IMPS
            - Digital banking
            - Fees & charges
            - Fraud & security
            """
        )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

question = st.chat_input("Ask a banking question...")


if question:

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(question)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            try:
                answer, _, _ = ask_banking_assistant(question)

                if not answer:
                    answer = "I couldn't find an answer to that question."

                st.markdown(answer)

            except Exception as e:

                answer = (
                    "Something went wrong while processing your question. "
                    "Please try again."
                )

                st.error(answer)

                print("\n[RAG ERROR]")
                print(e)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )