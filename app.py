import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
# Split large text into chunks so embeddings / retrieval work efficiently
#STEP 1: text splitter - Chunking using CharacterTextSplitter - to split large text
from langchain.text_splitter import CharacterTextSplitter
# Ollama text embeddings adapter (creates vector representations of text chunks)
#STEP 2: embeddings usinhg OllamaEmbeddings - to connect to Ollama embeddings model
from langchain_community.embeddings import OllamaEmbeddings 
# FAISS vector store to index and search embeddings locally
#STEP 3: vector store using FAISS - to store and retrieve embeddings
from langchain.vectorstores import FAISS
# Conversation memory to keep chat history between user and model
#STEP 4: memory to store conversation history - ConversationBufferMemory
from langchain.memory import ConversationBufferMemory
# Chain that wires an LLM with a retriever for conversational QA over documents
#STEP 5: conversational retrieval chain - to connect LLM and retriever
from langchain.chains import ConversationalRetrievalChain
# Chat model adapter for Ollama (to call the chosen Ollama LLM)
#STEP 6: chat model using ChatOllama - to connect to Ollama LLMs
from langchain_community.chat_models import ChatOllama
# HTML templates for rendering user/bot messages and page CSS
from htmlTemplates import bot_template, user_template, css

# ------------------ Helper Functions ------------------

def get_pdf_text(pdf_files):
    """Extract text from uploaded PDF files"""
    text = ""
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

#spilitter 
def get_chunk_text(text):
    """Split text into manageable chunks"""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

#Embeddings and Vector Store model :nomic-embed-text 
def get_vector_store(text_chunks):
    """Create FAISS vector store using Ollama embeddings"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Model Conversational Retrieval Chain - Model : mistral
def get_conversation_chain(vector_store, model_name="mistral"):
    llm = ChatOllama(
        model=model_name,
        temperature=0.45,
        num_ctx=4096  # larger context window helps
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}),
        memory=memory
    )

    return chain

# Clean LLM output text
def clean_text(text):
    """Remove unreadable control characters from LLM output"""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    elif not isinstance(text, str):
        text = str(text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.strip()

# Handle user input and display chat messages
def handle_user_input(question):
    """Handle and display chat messages"""
    try:
        response = st.session_state.conversation({'question': question})
        st.session_state.chat_history = response.get('chat_history', [])

        for i, msg in enumerate(st.session_state.chat_history):
            content = clean_text(msg.content)
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", content), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error while processing your question: {str(e)}")












# ------------------ Main App ------------------

def main():
    load_dotenv()
    st.set_page_config(
        page_title='Academic Document Query Bot',
        page_icon='🤖',
        layout="wide"           
    )

    st.markdown(css, unsafe_allow_html=True)

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Main Title
    st.markdown(
        "<h1 style='text-align:center; color:#00E5FF; '>"
        "Academic Document Query Bot</h1>"
        "<p style='text-align:center; color:#9B9B9B;'>✨Powered by Ollama</p>",
        unsafe_allow_html=True
    )

    # Chat input area
    question = st.text_input("Ask anything about your PDF:", placeholder="Type your question here and press Enter...")

    if question and st.session_state.conversation is not None:
        handle_user_input(question)
    elif question and st.session_state.conversation is None:
        st.warning("⚠️ Please upload and process your PDFs first!")

    # Sidebar
    with st.sidebar:
        st.markdown("<h3 style='color:#00E5FF;'>📂 Upload Documents</h3>", unsafe_allow_html=True)
        pdf_files = st.file_uploader(
            "Upload your PDF(s):",
            type=['pdf'],
            accept_multiple_files=True
        )

        st.markdown("<br><h3 style='color:#9B00FF;'>⚙️ Settings</h3>", unsafe_allow_html=True)
        model_name = st.selectbox("Choose Ollama model:", ["mistral", "llama3", "phi3", "gemma"])

        if st.button("🚀 Process PDFs"):
            if pdf_files:
                with st.spinner("🧠 Reading and processing your PDFs..."):
                    raw_text = get_pdf_text(pdf_files)
                    text_chunks = get_chunk_text(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store, model_name)
                    st.success("✅ PDFs processed successfully! You can now chat below 👇")
            else:
                st.warning("⚠️ Please upload at least one PDF file first.")

    st.markdown("<br><br><p style='text-align:center; color:gray;'>Made by ＲΛＪ</p>", unsafe_allow_html=True)


# ------------------ Run App ------------------

if __name__ == '__main__':
    main()
