import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

# GunPark Bot Client Init
GunPark = Client(
    "GunParkBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
)

# Startup Message to Owner
@GunPark.on_message(filters.private & filters.user(OWNER_ID))
async def send_start_message(_, message):
    if message.from_user and str(message.from_user.id) == str(OWNER_ID):
        await message.reply("👑 GunPark is Live & Loaded My Queen!")

if __name__ == "__main__":
    print("🔥 GunPark Bot Starting...")
    GunPark.run()
