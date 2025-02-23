from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
)
import logging

from src.retriever import RagService
from src.llm import LLMService

rag_service = RagService()
llm_service = LLMService(rag_service)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text("Я могу отвечать на твои вопросы. Просто напиши мне что-нибудь.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Логируем ошибки, вызванные обновлениями."""
    logger.error(f"Update: {update} caused error: {context.error}")
    if update and update.message: # проверка update
        update.message.reply_text("Произошла ошибка при обработке запроса.")


async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    # keyboard = [[InlineKeyboardButton("Задать вопрос", callback_data="ask")]]
    # reply_markup = InlineKeyboardMarkup(keyboard)   reply_markup=reply_markup
    await update.message.reply_text("Привет! Я бот-вопрошатель. Задавай вопросы!")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений (вопросов)."""
    question = update.message.text
    answer = llm_service.generate_answer(question)
    await update.message.reply_text(answer)


def setup_handlers(application):
    """Добавляем обработчики в приложение"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)