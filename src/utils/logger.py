import logging
import os

def setup_logging():
    """Настройка логирования."""
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        format="{asctime} | {levelname} | {name} | {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        level="INFO",
        style="{",
        filename="logs/bot.log",
        filemode="w",
        encoding="utf-8"
    )
