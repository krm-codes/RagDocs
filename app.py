import streamlit as st
from document_processor import DocumentProcessor
from chat_manager import ChatManager
import config

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

def main():
    st.title("RAG Chat Application")
    
    initialize_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        model_choice = st.radio(
            "Select Model",
            ["ollama", "openai"],
            help="Choose between Ollama (ChatGroq) and OpenAI"
        )
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            accept_multiple_files=True,
            type=["pdf"],
            help="Upload PDF files for processing"
        )
        
        if uploaded_files:
            if st.button("Process Documents"):
                with st.spinner("Processing documents..."):
                    processor = DocumentProcessor(model_choice)
                    st.session_state.vectorstore = processor.process_documents(uploaded_files)
                    if st.session_state.vectorstore:
                        st.success("Documents processed successfully!")
                    
    # Main chat interface
    if st.session_state.vectorstore is None:
        st.info("Please upload and process documents to start chatting.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source.page_content[:200]}...")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_manager = ChatManager(st.session_state.vectorstore, model_choice)
                response, sources = chat_manager.get_response(
                    prompt,
                    st.session_state.chat_history
                )
                
                if response:
                    st.write(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources
                    })
                    st.session_state.chat_history.append((prompt, response))

if __name__ == "__main__":
    main()
