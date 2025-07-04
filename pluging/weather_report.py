from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API")  # Use from .env or config.py

# Emoji Map
def get_weather_icon(desc):
    desc = desc.lower()
    if "clear" in desc:
        return "☀️"
    elif "cloud" in desc:
        return "☁️"
    elif "rain" in desc or "drizzle" in desc:
        return "🌧️"
    elif "thunder" in desc:
        return "⛈️"
    elif "snow" in desc:
        return "❄️"
    else:
        return "🌫️"

@Client.on_message(filters.command("weather"))
async def weather_report(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("🌤️ Use: `/weather <city>`\nExample: `/weather Mumbai`")

    city = " ".join(message.command[1:])
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return await message.reply("❌ City not found. Try again with a valid name.")

        name = res["name"]
        country = res["sys"]["country"]
        temp = res["main"]["temp"]
        humidity = res["main"]["humidity"]
        wind = res["wind"]["speed"]
        desc = res["weather"][0]["description"]
        icon = get_weather_icon(desc)

        await message.reply(
            f"🌍 **Weather in {name}, {country}**\n\n"
            f"{icon} *{desc.title()}*\n"
            f"🌡️ Temperature: `{temp}°C`\n"
            f"💧 Humidity: `{humidity}%`\n"
            f"💨 Wind: `{wind} m/s`"
        )

    except Exception as e:
        await message.reply("⚠️ Failed to get weather. Try again later.")
        print("Weather Error:", e)
