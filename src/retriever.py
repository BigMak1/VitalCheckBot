from langchain_gigachat.embeddings.gigachat import GigaChatEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

from src.config import settings


class RagService:
    def __init__(self):
        self.embedding_function = GigaChatEmbeddings(credentials=settings.gigachat.api_key, model="Embeddings", verify_ssl_certs=False)
        self.vectorstore = Chroma(embedding_function=self.embedding_function, persist_directory="data/retrivial_embeddings/chroma_db/") 

    def retrieve_context(self, query: str, top_k: int = 3) -> list[Document]:
        """Извлекает наиболее релевантные фрагменты текста из ChromaDB."""

        docs = self.vectorstore.similarity_search(query, k=top_k)
        return docs
