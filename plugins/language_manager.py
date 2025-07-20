from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
import json, os

translator = Translator()
LANG_FILE = "data/user_languages.json"

if os.path.exists(LANG_FILE):
    with open(LANG_FILE, "r") as f:
        user_lang = json.load(f)
else:
    user_lang = {}

supported_langs = {
    "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh-cn": "Chinese", "ja": "Japanese",
    "ko": "Korean", "tr": "Turkish", "ar": "Arabic", "bn": "Bengali", "ur": "Urdu",
    "ta": "Tamil", "te": "Telugu", "ml": "Malayalam", "id": "Indonesian", "vi": "Vietnamese",
    "th": "Thai", "tl": "Filipino", "uk": "Ukrainian", "pl": "Polish", "nl": "Dutch", "el": "Greek"
}

def save_lang():
    with open(LANG_FILE, "w") as f:
        json.dump(user_lang, f, indent=2)

@Client.on_message(filters.command("language"))
async def set_language(_, message: Message):
    user_id = str(message.from_user.id)
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        langs = "\n".join([f"`{k}` - {v}" for k, v in supported_langs.items()])
        return await message.reply(
            "🌐 Use: `/language <lang_code>`\n\n🗣️ *Available Languages:*\n" + langs
        )
    code = parts[1].strip().lower()
    if code not in supported_langs:
        return await message.reply("❌ Unsupported language code. Use `/language` to see list.")
    user_lang[user_id] = code
    save_lang()
    await message.reply(f"✅ Language set to *{supported_langs[code]}* (`{code}`)")

async def auto_translate(user_id: str, text: str):
    lang = user_lang.get(str(user_id), "en")
    translated = translator.translate(text, dest=lang)
    return translated.text
