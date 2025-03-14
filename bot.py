import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from api import TOKEN
from currency import convert_currency

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)

def get_currency_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="EUR"), KeyboardButton(text="USD")],
            [KeyboardButton(text="KZT"), KeyboardButton(text="Другое")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=main_keyboard)

@dp.message(Command("help"))
@dp.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    help_text = "📌 Доступные команды:\n/start - Начать работу с ботом\n/help - Список команд"
    await message.answer(help_text)

@dp.message(lambda message: message.text == "Начать")
async def start_conversion(message: types.Message):
    user_data[message.from_user.id] = {"step": "choose_from_currency"}
    await message.answer("Выберите валюту, из которой хотите конвертировать:", reply_markup=get_currency_keyboard())

@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("step") == "choose_from_currency")
async def choose_from_currency(message: types.Message):
    if message.text == "🔙 Назад":
        await cmd_start(message)
        return

    if message.text in ["EUR", "USD", "KZT"]:
        user_data[message.from_user.id]["from_currency"] = message.text
        user_data[message.from_user.id]["step"] = "enter_amount"
        await message.answer("Введите сумму:")
    elif message.text == "Другое":
        user_data[message.from_user.id]["step"] = "enter_from_currency_custom"
        await message.answer("Введите код вашей валюты (например, RUB, GBP, JPY):")

@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("step") == "enter_from_currency_custom")
async def enter_from_currency_custom(message: types.Message):
    if message.text == "🔙 Назад":
        user_data[message.from_user.id]["step"] = "choose_from_currency"
        await message.answer("Выберите валюту:", reply_markup=get_currency_keyboard())
        return

    user_data[message.from_user.id]["from_currency"] = message.text.upper()
    user_data[message.from_user.id]["step"] = "enter_amount"
    await message.answer("Введите сумму:")

# 6️⃣ Ввд суммы
@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("step") == "enter_amount")
async def enter_amount(message: types.Message):
    if message.text == "🔙 Назад":
        user_data[message.from_user.id]["step"] = "choose_from_currency"
        await message.answer("Выберите валюту:", reply_markup=get_currency_keyboard())
        return

    user_data[message.from_user.id]["amount"] = float(message.text)
    user_data[message.from_user.id]["step"] = "choose_to_currency"
    await message.answer("Выберите валюту, в которую хотите перевести:", reply_markup=get_currency_keyboard())

@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("step") == "choose_to_currency")
async def choose_to_currency(message: types.Message):
    if message.text == "🔙 Назад":
        user_data[message.from_user.id]["step"] = "enter_amount"
        await message.answer("Введите сумму:")
        return

    if message.text in ["EUR", "USD", "KZT"]:
        user_data[message.from_user.id]["to_currency"] = message.text
        await perform_conversion(message)
    elif message.text == "Другое":
        user_data[message.from_user.id]["step"] = "enter_to_currency_custom"
        await message.answer("Введите код целевой валюты (например, RUB, GBP, JPY):")

@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("step") == "enter_to_currency_custom")
async def enter_to_currency_custom(message: types.Message):
    if message.text == "🔙 Назад":
        user_data[message.from_user.id]["step"] = "choose_to_currency"
        await message.answer("Выберите валюту:", reply_markup=get_currency_keyboard())
        return

    user_data[message.from_user.id]["to_currency"] = message.text.upper()
    await perform_conversion(message)

async def perform_conversion(message: types.Message):
    user_id = message.from_user.id
    data = user_data.get(user_id, {})
    from_currency = data.get("from_currency")
    amount = data.get("amount")
    to_currency = data.get("to_currency")
    result = await convert_currency(amount, from_currency, to_currency)

    if result is not None:
        formatted_amount = "{:,}".format(int(amount)).replace(",", " ")  
        formatted_result = "{:,}".format(int(result)).replace(",", " ")  
        await message.answer(f"{formatted_amount} {from_currency} = {formatted_result} {to_currency}")
    else:
        await message.answer("Ошибка при конвертации. Проверьте коды валют.")
    
    user_data.pop(user_id, None)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
