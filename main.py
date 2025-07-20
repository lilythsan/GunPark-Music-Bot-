import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped, HighQualityAudio
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from config import API_ID, API_HASH, SESSION_STRING

# Initialize Pyrogram and PyTgCalls
app = Client("GunPark", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(app)

# Function to search and download YouTube audio
def download_audio(query):
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()["result"][0]
    url = result["link"]

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title).20s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "extractaudio": True,
        "audioformat": "mp3",
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# /play command
@app.on_message(filters.command("play"))
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply("❗ Song name do, jaise /play kesariya")
        return

    song_name = " ".join(message.command[1:])
    msg = await message.reply(f"🔎 Searching: *{song_name}*")

    try:
        file_path = download_audio(song_name)
        await call_py.join_group_call(
            chat_id=message.chat.id,
            input_stream=AudioPiped(file_path, HighQualityAudio())
        )
        await msg.edit(f"▶ Playing: *{song_name}*")
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

# /leave command
@app.on_message(filters.command("leave"))
async def leave_vc(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("👋 Left VC.")
        for file in os.listdir():
            if file.endswith(".webm") or file.endswith(".mp3"):
                os.remove(file)
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
