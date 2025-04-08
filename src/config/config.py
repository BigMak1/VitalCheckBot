import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class TelegramConfig(BaseModel):
    bot_token: str


class OpenaiConfig(BaseModel):
    api_key: str
    proxy_url: str
    chat_model: str = "gpt-4o-mini"
    embeddings_model: str = "text-embedding-3-large"


class GigachatConfig(BaseModel):
    api_key: str
    model: str = "GigaChat-2-Max"


class LangsmithConfig(BaseModel):
    api_key: str
    tracing: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        # env_prefix="FASTAPI__",
        env_file=("../.env", ".env"),
        extra = "ignore"
    )
    telegram: TelegramConfig
    openai: OpenaiConfig
    gigachat: GigachatConfig
    langsmith: LangsmithConfig


settings = Settings()
os.environ["LANGSMITH_API_KEY"] = settings.langsmith.api_key
os.environ["LANGSMITH_TRACING"] = settings.langsmith.tracing