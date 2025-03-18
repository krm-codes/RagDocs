from typing import List
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import config

class ChatManager:
    def __init__(self, vectorstore, model_choice: str):
        self.vectorstore = vectorstore
        self.model_choice = model_choice
        self.llm = self._get_llm()
        self.chain = self._create_chain()

    def _get_llm(self):
        if self.model_choice == "ollama":
            return ChatGroq(
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                model_name=config.AVAILABLE_MODELS["ollama"],
                groq_api_key=config.OPENAI_API_KEY  # Groq uses OpenAI-compatible API
            )
        return ChatOpenAI(
            temperature=config.TEMPERATURE,
            model_name=config.AVAILABLE_MODELS["openai"],
            openai_api_key=config.OPENAI_API_KEY
        )

    def _create_chain(self):
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )

    def get_response(self, query: str, chat_history: List) -> tuple:
        try:
            result = self.chain({"question": query, "chat_history": chat_history})
            return result["answer"], result["source_documents"]
        except Exception as e:
            st.error(f"Error getting response: {str(e)}")
            return None, None