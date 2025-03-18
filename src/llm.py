from langchain_gigachat.chat_models import GigaChat
from langchain.chains import RetrievalQA, create_retrieval_chain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import logging

from src.config.config import settings
from src.retriever import RagService

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, rag_service: RagService):
        self.llm = GigaChat(
            credentials=settings.llm.gigachat_credentials,
            model=settings.llm.gigachat_model,
            scope=settings.llm.gigachat_scope,
            verify_ssl_certs=settings.llm.gigachat_verify_ssl_certs
        )
        self.rag_service = rag_service
        logger.debug("LLMService initialized.") # Логируем инициализацию

        # Шаблон промпта (важная часть!)
        self.system_prompt = (
            "Ты - полезный ассистент, который отвечает на вопросы, опираясь на предоставленный контекст.\n"
            "Если ты не можешь ответить, используя только контекст, скажи, что не знаешь и нужно обратиться к Дементьеву Александру.\n"
            "Контекст:"
            "\n\n"
            "{context}"
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{input}"),
            ]
        )


    def generate_answer(self, question: str) -> str:
        """Генерирует ответ на вопрос, используя LLM и RAG."""

        logger.info(f'Вопрос пользователя: {question}')

        # 1. Получаем контекст из RAG
        context_documents = self.rag_service.retrieve_context(query=question, top_k=1)
        context = "\n\n".join([doc.page_content for doc in context_documents])

        logger.info(f'Контекст из RAG: {context}')

        # 2. Формируем промпт
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt_template)

        # # 3. Создаем цепочку и запускаем
        rag_chain = create_retrieval_chain(self.rag_service.vectorstore.as_retriever(), question_answer_chain)
        response = rag_chain.invoke({"input": question})["answer"]

        logger.info(f'Ответ LLM после RAG: {response}')

        return response