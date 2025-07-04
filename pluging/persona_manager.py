from pyrogram import Client, filters
from pyrogram.types import Message
import json, os

PERSONA_FILE = "data/personas.json"

# Load memory file
if os.path.exists(PERSONA_FILE):
    with open(PERSONA_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(PERSONA_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# 📌 /createpersona
@Client.on_message(filters.command("createpersona"))
async def create_persona(_, message: Message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return await message.reply("❗Use: /createpersona <Name> <Mood>\nExample: `/createpersona Akari flirty`")
        name, mood = parts[1], parts[2]
        user_id = str(message.from_user.id)
        memory[user_id] = {"name": name, "mood": mood}
        save_memory()
        await message.reply(f"✅ *Persona created!*\nYour waifu/villain `{name}` with mood `{mood}` is now active.")
    except Exception as e:
        await message.reply("❌ Failed to create persona.")
        print(e)

# 🧠 /mywaifu
@Client.on_message(filters.command("mywaifu"))
async def talk_to_waifu(_, message: Message):
    user_id = str(message.from_user.id)
    if user_id not in memory:
        return await message.reply("👤 You haven't created a waifu/villain yet. Use `/createpersona` first.")
    persona = memory[user_id]
    reply = f"❤️ *{persona['name']}* ({persona['mood']} mode):\n"
    reply += f"`{message.text[8:].strip() or 'You look cute today... ♥'}`"
    await message.reply(reply)

# ❌ /deletepersona
@Client.on_message(filters.command("deletepersona"))
async def delete_persona(_, message: Message):
    user_id = str(message.from_user.id)
    if user_id in memory:
        del memory[user_id]
        save_memory()
        await message.reply("🗑️ Your persona has been deleted.")
    else:
        await message.reply("You didn't have any saved persona.")
