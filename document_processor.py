from typing import List
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings as OAIEmbeddings
import tempfile
import os
import config

class DocumentProcessor:
    def __init__(self, model_choice: str):
        self.model_choice = model_choice
        self.embeddings = self._get_embeddings()

    def _get_embeddings(self):
        if self.model_choice == "ollama":
            # Use OpenAI's embeddings for both since Groq doesn't provide embeddings yet
            return OAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        return OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    def process_documents(self, uploaded_files) -> FAISS:
        documents = []

        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file.flush()

                try:
                    if file.name.endswith('.pdf'):
                        loader = PyPDFLoader(tmp_file.name)
                        documents.extend(loader.load())
                    else:
                        st.error(f"Unsupported file type: {file.name}")
                except Exception as e:
                    st.error(f"Error processing file {file.name}: {str(e)}")
                finally:
                    os.unlink(tmp_file.name)

        if not documents:
            return None

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

        texts = text_splitter.split_documents(documents)

        try:
            vectorstore = FAISS.from_documents(texts, self.embeddings)
            return vectorstore
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            return None