import aiohttp

API_KEY = "cur_live_amudzKTSGdzlegM7KbiJs3XVbsuBha8iuxcu3qiZ"
API_URL = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}"

async def convert_currency(amount, from_currency, to_currency):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            data = await resp.json()
            rates = data.get("data", {})

            if from_currency in rates and to_currency in rates:
                return round((amount / rates[from_currency]["value"]) * rates[to_currency]["value"], 2)
            return None
