from pyrogram import Client, filters
import config

app = Client(
    "GunParkBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply_text(f"Hello {message.from_user.first_name}!\nGun Park is alive and ready! 🧠")

app.run()