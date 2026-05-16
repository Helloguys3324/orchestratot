import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN
from filters.profanity_filter import ProfanityFilter

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Список матных слов (лучше вынести в файл или БД)
BAD_WORDS = ["мат1", "мат2", "плохоеслово"] 
profanity_filter = ProfanityFilter(BAD_WORDS)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот запущен и следит за чистотой чата!")

@dp.message()
async def check_messages(message: Message):
    if message.text and profanity_filter.contains_profanity(message.text):
        await message.delete()
        await message.answer(f"@{message.from_user.username}, мат запрещен!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())