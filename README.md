# RAG-banking-assistant

An AI-powered banking support assistant that answers questions using a controlled knowledge base of fictional banking policy documents.

Built as a learning and portfolio project to explore **RAG, LLMs, and reliable AI application development.**

## ✨ How It Works

1. **Load documents:** Read banking policy documents in Markdown format.
2. **Chunk & embed:** Split documents into smaller pieces and convert them into embeddings.
3. **Retrieve:** Find relevant policy chunks based on the user's question.
4. **Generate:** Use the retrieved context to generate a grounded answer.
5. **Validate:** Check the response structure and attach citations from the retrieved sources.
6. **Refuse or escalate:** If the information is insufficient or the issue needs support, the assistant can refuse or route it for escalation.

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain & LangGraph
* ChromaDB
* Hugging Face Embeddings
* Pydantic
* SQLite

## 🎯 Project Goals

* Reduce unsupported AI answers through retrieval and validation.
* Provide answers with policy-document citations.
* Handle unsupported and sensitive questions safely.
* Explore evaluation metrics such as groundedness, retrieval relevance, refusal accuracy, and response latency.

## 📁 Knowledge Base

The project uses 18 fictional banking policy documents covering accounts, cards, transfers, loans, KYC, fees, fraud, and customer support.

## ⚠️ Disclaimer

This is an educational project using fictional banking information. It does not connect to real bank accounts, process transactions, or provide personalized financial advice.

## 🚧 Status

Currently under development. Features and evaluation results will be updated as implementation progresses.

