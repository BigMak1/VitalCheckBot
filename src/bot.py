# from config.config import BOT_TOKEN
# from src.rag import get_response

# import logging
# import sys

# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram import Bot, Dispatcher, types
# # from aiogram.utils import executor

# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()

# @dp.message(CommandStart())
# async def handle_message(message: types.Message):
#     response = get_response(message.text)
#     await message.answer(response)

# def start_bot() -> None:
#     dp.start_polling(bot)
#     # executor.start_polling(dp, skip_updates=True)
