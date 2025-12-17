# 📚 Academic Document Query Bot

A **local, privacy-first AI application** that enables users to chat with academic PDF documents using **Retrieval-Augmented Generation (RAG)**.

Built with **Streamlit, LangChain, FAISS, and Ollama**, this project runs entirely on **locally hosted Large Language Models (LLMs)** — **no OpenAI, no cloud APIs**.

---

## 🚀 Features

- Upload and process academic PDF documents
- Ask natural-language questions about uploaded content
- Retrieval-Augmented Generation (RAG) pipeline
- Local embeddings and inference using Ollama
- Conversational chat interface with memory
- Multiple local model support
- Clean and modern Streamlit UI

---

## 🛠️ Tech Stack

| Category | Technology |
|--------|-----------|
| Frontend | Streamlit |
| LLM Runtime | Ollama (Local) |
| Framework | LangChain |
| Embeddings | nomic-embed-text |
| Vector Store | FAISS |
| PDF Parsing | PyPDF2 |
| Language | Python |

---

## 🧠 How It Works (Architecture)

PDF Upload  
    ↓  
Text Extraction (PyPDF2)  
    ↓  
Text Chunking  
    ↓  
Vector Embeddings (Ollama)  
    ↓  
FAISS Vector Store  
    ↓  
Conversational Retrieval Chain  
    ↓  
Local LLM Response (Ollama)

This pipeline ensures responses are **grounded in the uploaded documents**, improving accuracy and relevance.

---

## 📸 Screenshots

### Home Screen
<img src="https://github.com/user-attachments/assets/ec2e336e-e7d4-48b6-9959-e5ab76fb6400" width="75%" />

### Chat Interface
<img src="https://github.com/user-attachments/assets/789cfebe-9c6a-4840-bd5a-746ffb6b21b0" width="75%" />


---

## ⚙️ Requirements

- Python 3.11+
- Ollama installed and running locally
- At least one Ollama model pulled

---

## 📦 Supported Ollama Models

- mistral
- llama3
- phi3
- gemma

Embeddings model:
- nomic-embed-text

---

## 🧩 Installation & Setup

### Install Ollama
https://ollama.com

```bash
ollama pull nomic-embed-text
ollama pull mistral
ollama pull llama3
ollama pull phi3
ollama pull gemma


