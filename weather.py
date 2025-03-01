import requests

API_KEY = "7f92074688f56f88b2a27aa0ce71316a"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
city = "Almaty"

response = requests.get(f"{WEATHER_URL}?q={city}&appid={API_KEY}&units=metric")
data = response.json()

print(data)

async def get_weather(city:str):
    params = {
        "q":  "Алматы",
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as responce:
            data = await responce.json()
            if responce.status == 200:
                return ( 
                    f"Temperature in {city}: {data['main']['temp']} C\n"\
                    f"Ветер: {data['wind']['speed']}м/с\n"\
                    f"Погода: {data['weather'][0]['description'].capitalize()}"
                )
            else:
                return "Ошибка. Не удалось получить погодуь для Алматы"
                       