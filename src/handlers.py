from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler
)
import logging
import json
import os
from datetime import datetime

from src.retriever import RagService
from src.llm import LLMService

rag_service = RagService()
llm_service = LLMService(rag_service)

logger = logging.getLogger(__name__)

# Пути к файлам для сохранения статистики и дизлайков
STATS_FILE = "feedback_stats.json"
DISLIKES_FILE = "disliked_responses.json"


# Загрузка статистики из файла
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"likes": 0, "dislikes": 0}


# Сохранение статистики в файл
def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)


# Загрузка дизлайкнутых ответов
def load_dislikes():
    if os.path.exists(DISLIKES_FILE):
        with open(DISLIKES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Сохранение дизлайкнутых ответов
def save_dislike(question, answer, user_id, username):
    dislikes = load_dislikes()
    dislikes.append({
        "question": question,
        "answer": answer,
        "user_id": user_id,
        "username": username,
        "timestamp": datetime.now().isoformat()
    })
    with open(DISLIKES_FILE, "w", encoding="utf-8") as f:
        json.dump(dislikes, f, ensure_ascii=False, indent=2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я могу отвечать на твои вопросы. Просто напиши мне что-нибудь.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Логируем ошибки, вызванные обновлениями."""
    logger.error(f"Update: {update} caused error: {context.error}")
    if update and update.message:
        update.message.reply_text("Произошла ошибка при обработке запроса.")


async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    # Новое приветственное сообщение
    welcome_message = (
        "Привет! 👋 Я — твой ИИ помощник, созданный для работы с юридическим подразделением. Сейчас я знаю все, что касается технологической схемы по работе с описками.\n\n"
        "Просто напиши мне свой вопрос, и я постараюсь дать максимально полезный ответ.\n\n"
        "Ты можешь поставить 👍 или 👎, чтобы помочь мне стать лучше!"
    )
    await update.message.reply_text(welcome_message)


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений (вопросов)."""
    question = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name

    # Сохраняем вопрос в контексте для последующего использования
    context.user_data["last_question"] = question

    answer = llm_service.generate_answer(question)

    # Добавляем кнопки для лайков и дизлайков
    keyboard = [
        [InlineKeyboardButton("👍", callback_data=f"like_{answer[:10]}"),
         InlineKeyboardButton("👎", callback_data=f"dislike_{answer[:10]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_message = await update.message.reply_text(answer, reply_markup=reply_markup)

    # Сохраняем ответ в контексте для последующего использования
    context.user_data["last_answer"] = answer
    context.user_data["last_user_id"] = user_id
    context.user_data["last_username"] = username


async def handle_feedback(update: Update, context: CallbackContext) -> None:
    """Обработчик лайков и дизлайков."""
    query = update.callback_query
    await query.answer()  # Подтверждаем обработку callback-запроса

    # Извлекаем тип фидбека (лайк или дизлайк) и идентификатор ответа
    feedback_type, answer_id = query.data.split("_")

    # Загружаем текущую статистику
    stats = load_stats()

    # Обновляем статистику
    if feedback_type == "like":
        stats["likes"] += 1
    elif feedback_type == "dislike":
        stats["dislikes"] += 1

        # Сохраняем дизлайкнутый ответ
        if "last_question" in context.user_data and "last_answer" in context.user_data:
            question = context.user_data.get("last_question", "")
            answer = context.user_data.get("last_answer", "")
            user_id = context.user_data.get("last_user_id", query.from_user.id)
            username = context.user_data.get("last_username", query.from_user.username or query.from_user.first_name)
            save_dislike(question, answer, user_id, username)

    # Сохраняем обновленную статистику
    save_stats(stats)

    # Убираем кнопки после нажатия
    await query.edit_message_reply_markup(reply_markup=None)

    # Отправляем отдельное сообщение с благодарностью за фидбек
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"Спасибо за ваш фидбек! 🎉\n(Лайков: {stats['likes']}, Дизлайков: {stats['dislikes']})"
    )


async def get_disliked_responses(update: Update, context: CallbackContext) -> None:
    """Команда для получения списка дизлайкнутых ответов (только для админов)."""
    # Список ID администраторов (вставьте свои ID)
    admin_ids = [12345, 67890]  # Замените на реальные ID администраторов

    user_id = update.message.from_user.id
    if user_id not in admin_ids:
        await update.message.reply_text("У вас нет доступа к этой команде.")
        return

    dislikes = load_dislikes()
    if not dislikes:
        await update.message.reply_text("Пока нет дизлайкнутых ответов.")
        return

    # Формируем сообщение с последними 5 дизлайкнутыми ответами
    response = "Последние дизлайкнутые ответы:\n\n"
    for i, dislike in enumerate(dislikes[-5:], 1):
        date = datetime.fromisoformat(dislike["timestamp"]).strftime("%d.%m.%Y %H:%M")
        response += f"{i}. Дата: {date}\n"
        response += f"Пользователь: {dislike['username']} (ID: {dislike['user_id']})\n"
        response += f"Вопрос: {dislike['question']}\n"
        response += f"Ответ: {dislike['answer'][:100]}...\n\n"

    await update.message.reply_text(response)


def setup_handlers(application):
    """Добавляем обработчики в приложение"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dislikes", get_disliked_responses))  # Новая команда
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_feedback))
    application.add_error_handler(error)