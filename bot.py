from pyrogram import Client, filters
import config

app = Client("GunParkBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply_text(f"Hello {message.from_user.first_name}!\nGun Park is alive and ready! 🧠")

app.run()
from pyrogram.types import Message
from pytube import YouTube
import os

@app.on_message(filters.command("yt") & filters.private)
def youtube_downloader(client, message: Message):
    if len(message.command) < 2:
        message.reply_text("🔗 YouTube link bhejo is format me:\n`/yt <youtube-link>`")
        return

    url = message.command[1]
    message.reply_text("⏳ Downloading video...")

    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        file_path = stream.download(filename="yt_audio.mp4")

        message.reply_audio(
            audio=file_path,
            caption=f"🎶 {yt.title}",
            performer=yt.author,
            title=yt.title
        )

        os.remove(file_path)
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
