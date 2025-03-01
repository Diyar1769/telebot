import aiohttp
import os

API_KEY = "7f92074688f56f88b2a27aa0ce71316a"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str):
    params = {
        "q": city,  # Передаем название города из аргумента функции
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as response:
            data = await response.json()
            if response.status == 200:
                return (
                    f"Температура в {city}: {data['main']['temp']} C\n"
                    f"Ветер: {data['wind']['speed']} м/с\n"
                    f"Погода: {data['weather'][0]['description'].capitalize()}"
                )
            else:
                return f"Ошибка. Не удалось получить погоду для города {city}"

