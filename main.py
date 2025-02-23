import logging
from telegram.ext import Application
from src.config.config import settings
from src.handlers import setup_handlers
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)

def main():
    app = Application.builder().token(settings.telegram_bot_token).build()
    setup_handlers(app)
    print("Bot is running ...")
    app.run_polling()


if __name__ == "__main__":
    setup_logging()  # Настраиваем логирование
    logger.info("Starting the bot application...")  # Логируем старт приложения
    main()