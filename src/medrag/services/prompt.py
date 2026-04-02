from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = (
    "You are a helpful medical professional assistant for answering questions.\n\n"
    "Answer the question based on retrieved medical context.\n\n"
    "If the answer is not present in context, say you do not know.\n\n"
    "Keep responses concise and clear.\n\n"
    "{context}"
)


def build_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", "{input}")]
    )
