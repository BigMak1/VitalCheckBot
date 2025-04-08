from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import constants
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
)
import logging

from src.llm_assistant import process_query

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text("Я могу отвечать на твои вопросы. Просто напиши мне что-нибудь.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Логируем ошибки, вызванные обновлениями."""
    logger.error(f"Сaused error: {context.error}")
    if update and update.message:
        update.message.reply_text("Произошла ошибка при обработке запроса.")


async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text("Привет! Я бот-вопрошатель. Задавай вопросы!")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений (вопросов)."""

    # Добавляем процесс что бот печатает ответ
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)

    user_message = update.message.text
    thread_config = {"configurable": {"thread_id": update.message.chat.id}}

    result = process_query(stream_input=user_message, thread_config=thread_config)
    response = result["response"]
    logger.info(f"Final response to user in tg: {response}")
    await update.message.reply_text(response, parse_mode="Markdown")


def setup_handlers(application):
    """Добавляем обработчики в приложение"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)