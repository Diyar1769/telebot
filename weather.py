import aiohttp
from api import API_KEY, WEATHER_URL

CITIES = {
    "Казахстан": ["Алматы", "Астана"],
    "Россия": ["Москва"]
}




async def get_weather(city: str = "Алматы"):
    params = { 
        "q": "city",  
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as response:
            data = await response.json()  
            if response.status == 200:  
                return (
                    f"Температура в Алматы: {data['main']['temp']}°C\n"
                    f"Ветер: {data['wind']['speed']} м/с\n"
                    f"Погода: {data['weather'][0]['description'].capitalize()}"
                )
            else:
                return "Ошибка. Не удалось получить погоду для Алматы."

def get_available_cities():
    return CITIES
