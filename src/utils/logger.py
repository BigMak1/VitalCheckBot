import logging
from src.config.config import settings

def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        format="{asctime} | {levelname} | {name} | {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=settings.log_level,
        style="{",
        filename="logs/bot.log",
        filemode="w",
        encoding="utf-8"
    )
