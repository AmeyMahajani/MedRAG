from langchain_community.embeddings import HuggingFaceEmbeddings


def download_embeddings() -> HuggingFaceEmbeddings:
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)
