import os
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableLambda
from langchain_pinecone import PineconeVectorStore

from .embeddings import download_embeddings
from .prompt import build_rag_prompt


class RAGService:
    def __init__(self) -> None:
        load_dotenv()

        self.fake_mode = os.getenv("MEDRAG_FAKE_MODE", "false").lower() == "true"
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "medrag-index")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        self.enabled = False
        self.rag_chain = None

        if self.fake_mode:
            return

        if not self.pinecone_api_key or not self.gemini_api_key:
            return

        try:
            os.environ["PINECONE_API_KEY"] = self.pinecone_api_key
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key

            embeddings = download_embeddings()
            docsearch = PineconeVectorStore.from_existing_index(
                index_name=self.index_name,
                embedding=embeddings,
            )
            retriever = docsearch.as_retriever(
                search_type="similarity", search_kwargs={"k": 3}
            )

            genai.configure(api_key=self.gemini_api_key)
            gemini_model = genai.GenerativeModel(self.model_name)

            def run_gemini(prompt_value: Any) -> str:
                prompt_text = (
                    prompt_value.to_string()
                    if hasattr(prompt_value, "to_string")
                    else str(prompt_value)
                )
                return gemini_model.generate_content(prompt_text).text

            qa_chain = create_stuff_documents_chain(
                llm=RunnableLambda(run_gemini),
                prompt=build_rag_prompt(),
            )
            self.rag_chain = create_retrieval_chain(
                retriever=retriever,
                combine_docs_chain=qa_chain,
            )
            self.enabled = True
        except Exception:
            self.enabled = False
            self.rag_chain = None

    def ask(self, question: str) -> dict[str, Any]:
        clean_question = question.strip()
        if not clean_question:
            return {"answer": "Please ask a valid medical question."}

        if self.fake_mode:
            return {
                "answer": f"Demo mode response: I received your question - '{clean_question}'."
            }

        if not self.enabled or not self.rag_chain:
            return {
                "answer": "Service is not fully configured. Set API keys in .env and restart the app."
            }

        try:
            result = self.rag_chain.invoke({"input": clean_question})
            return {
                "answer": result.get("answer", "I could not generate an answer right now."),
            }
        except Exception:
            return {
                "answer": "I hit an internal error while generating the answer. Please try again.",
            }
