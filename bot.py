import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from api import TOKEN


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет!"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)


inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на сайт", url="http://example.com")],
        [InlineKeyboardButton(text="Нажми", callback_data="button_click")]
    ]
)

@dp.message(lambda message: message.text == "Помощь")
async def help_message(message: types.Message):
    await message.answer("Тебе нужная помощь?"
    )

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я тестовый бот <b>test</b>", reply_markup=main_keyboard)

@dp.message(lambda message: message.text == "Привет")
async def hello(message: types.Message):
    await message.answer("Привет!!! Как дела?", reply_markup=inline_keyboard)

@dp.message(Command("/help"))
async def help(message: types.Message):
    await message.answer("Тебе нужна помощь?", reply_markup=inline_keyboard)

async def main():
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == "__main__":
    asyncio.run(main())