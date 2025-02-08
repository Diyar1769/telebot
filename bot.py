import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from api import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Hello")


@dp.message(Command("help"))
async def send_help(message: Message):
    await message.answer("/help and /start are available")

 

async def main():
    print("Bot is ready")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
