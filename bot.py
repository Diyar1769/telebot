import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from weather import get_weather  # Функция для получения погоды
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
        [InlineKeyboardButton(text="Начать", callback_data="start")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Рандомное число", callback_data="random")]
    ]
)

# Обработчик callback кнопок
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "start":
        await callback.message.answer("Write /start")
    elif callback.data == "help":
        await callback.message.answer("Write /help")
    elif callback.data == "random":
        await callback.message.answer("Write random number: /random")

# Стартовая команда
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Что тебе нужно?", reply_markup=main_keyboard)

# Команда помощи
@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды: \n"
        "/start - Начать работу с ботом\n"
        "/help - Показать список команд\n"
        "/random - Случайное число\n"
        "/weather - Узнать погоду в городе"
    )
    await message.answer(command_text)

# Команда погоды
@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    # Запрашиваем у пользователя название города
    await message.answer("Введите название города, чтобы узнать погоду:")

    # Ожидаем ответа с названием города
    @dp.message()
    async def get_city(message: types.Message):
        city = message.text
        weather_info = await get_weather(city)  # Передаем название города
        await message.reply(weather_info)

# Команда случайного числа
@dp.message(Command("random"))
async def random_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")

# Приветственное сообщение
@dp.message(lambda message: message.text == "Привет!")
async def hello(message: types.Message):
    await message.answer("Привет! Ты нажал на кнопку", reply_markup=inline_keyboard)

# Сообщение помощи
@dp.message(lambda message: message.text == "Помощь")
async def help_message(message: types.Message):
    await message.answer("Тебе нужная помощь?")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
