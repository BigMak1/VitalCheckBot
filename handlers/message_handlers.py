from telegram import Update
from telegram.ext import ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    await update.message.reply_text(f'Вы написали: {message_text}')