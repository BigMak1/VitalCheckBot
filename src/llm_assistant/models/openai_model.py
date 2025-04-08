import httpx
from langchain_openai import ChatOpenAI

from src.config import settings


class OpenAIChatModel:
    def __init__(self, api_key=None, model=None, proxy_url=None, **kwargs):
        self.api_key = api_key or settings.openai.api_key
        self.model = model or settings.openai.chat_model
        self.http_client = httpx.Client(proxy=proxy_url or settings.openai.proxy_url)
        self.kwargs = kwargs

    def create_model(self):
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            http_client=self.http_client,
            **self.kwargs
        )