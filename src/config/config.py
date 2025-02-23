import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class LLMSettings(BaseSettings):
    """Настройки для LLM"""
    gigachat_credentials: str = Field(..., alias="GIGACHAT_CREDENTIALS")
    gigachat_scope: str = Field("GIGACHAT_API_PERS", alias="GIGACHAT_SCOPE")
    gigachat_model: str = Field("GigaChat-Max", alias="GIGACHAT_MODEL")
    gigachat_verify_ssl_certs: bool = Field(False, alias="GIGACHAT_VERIFY_SSL_CERTS")


class EmbeddingsSettings(BaseSettings):
    """Настройки для Embeddings"""
    embeddings_credentials: str = Field(..., alias="EMBEDDINGS_CREDENTIALS")
    embeddings_model: str = Field("Embeddings", alias="EMBEDDINGS_MODEL")


class Settings(BaseSettings):
    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")  # "..." означает, что поле обязательно 
    llm: LLMSettings = Field(default_factory=LLMSettings) # Добавляем вложенный объект настроек LLM
    embeddings: EmbeddingsSettings = Field(default_factory=EmbeddingsSettings)
    chroma_db_path: str = Field("retrivial_embeddings/chroma_db", alias="CHROMA_DB_PATH")
    log_level: str = Field("INFO", alias="LOG_LEVEL")  # Уровень логирования


settings = Settings()