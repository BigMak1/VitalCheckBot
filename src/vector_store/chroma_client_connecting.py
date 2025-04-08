import chromadb
from langchain_chroma import Chroma

from src.llm_assistant.models import OpenAIEmbeddingsModel

persistent_client = chromadb.PersistentClient(path="src/vector_store/chroma_db/")

embedding_function = OpenAIEmbeddingsModel().create_model()

vector_store_analysis = Chroma(client=persistent_client, collection_name="judicial_acts_analysis", embedding_function=embedding_function)
vector_store_procedures = Chroma(client=persistent_client, collection_name="rejection_procedures", embedding_function=embedding_function)