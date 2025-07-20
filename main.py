import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

from config import (
    API_ID,
    API_HASH,
    SESSION_STRING
)

# Pyrogram client
app = Client("GunPark", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# PyTgCalls client
call_py = PyTgCalls(app)

# /vcplay command
@app.on_message(filters.command("vcplay"))
async def vc_play(client, message):
    if len(message.command) < 2:
        await message.reply("❗ Song URL ya file path do.")
        return

    audio_path = message.command[1]
    try:
        await call_py.join_group_call(
            chat_id=message.chat.id,
            input_stream=AudioPiped(audio_path, HighQualityAudio())
        )
        await message.reply("▶ Playing in VC!")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# /vcleave command
@app.on_message(filters.command("vcleave"))
async def vc_leave(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("👋 Left VC.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# Start the bot
async def main():
    await app.start()
    await call_py.start()
    print("✅ Bot is running...")
    await app.idle()

if _name_ == "_main_":
    asyncio.run(main())
