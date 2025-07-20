import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls import InputAudioStream, AudioQuality
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from pytgcalls.exceptions import GroupCallNotFoundError
from config import API_ID, API_HASH, SESSION_STRING

# === Setup ===
app = Client("GunPark", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(app)

AUDIO_DIR = "./audios"
os.makedirs(AUDIO_DIR, exist_ok=True)
ALLOWED_EXTS = [".mp3", ".opus", ".wav", ".m4a"]

queues = {}  # chat_id: list of {"file": path, "title": name}
loop_enabled = {}  # chat_id: True/False


# === Helpers ===
def is_valid_audio(path: str) -> bool:
    ext = os.path.splitext(path)[-1].lower()
    return os.path.isfile(path) and ext in ALLOWED_EXTS


def add_to_queue(chat_id, file_path, title):
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append({"file": file_path, "title": title})


async def play_next(chat_id):
    if loop_enabled.get(chat_id):
        current = queues[chat_id][0]
        await call_py.join_group_call(
            chat_id,
            InputAudioStream(
                current["file"],
                audio_quality=AudioQuality.HIGH
            )
        )
        return

    if queues.get(chat_id):
        queues[chat_id].pop(0)

    if queues.get(chat_id):
        next_track = queues[chat_id][0]
        await call_py.join_group_call(
            chat_id,
            InputAudioStream(
                next_track["file"],
                audio_quality=AudioQuality.HIGH
            )
        )


@call_py.on_stream_end()
async def on_stream_end(_, update):
    chat_id = update.chat_id
    await play_next(chat_id)


# === YouTube Downloader ===
def download_audio(query):
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()["result"][0]
    url = result["link"]
    title = result["title"]

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
        return filename, title


# === Commands ===

@app.on_message(filters.command("play"))
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply("❗ Song name do, jaise /play kesariya")
        return

    song_name = " ".join(message.command[1:])
    msg = await message.reply(f"🔎 Searching: {song_name}")

    try:
        file_path, title = download_audio(song_name)
        add_to_queue(message.chat.id, file_path, title)

        if not call_py.get_call(message.chat.id):
            await play_next(message.chat.id)
            await msg.edit(f"▶ Playing: {title}")
        else:
            await msg.edit(f"✅ Added to queue: {title}")
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")


@app.on_message(filters.command("vcplay"))
async def vc_play(client, message):
    if len(message.command) < 2:
        await message.reply("❗ Provide a filename from /audios (e.g., song.mp3)")
        return

    filename = message.command[1]
    audio_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.abspath(audio_path).startswith(os.path.abspath(AUDIO_DIR)):
        await message.reply("🚫 Invalid filename.")
        return

    if not is_valid_audio(audio_path):
        await message.reply("❌ File doesn't exist or unsupported format.")
        return

    add_to_queue(message.chat.id, audio_path, filename)

    if not call_py.get_call(message.chat.id):
        await play_next(message.chat.id)
        await message.reply(f"▶ Now playing: {filename}")
    else:
        await message.reply(f"✅ Added to queue: {filename}")


@app.on_message(filters.command(["vcstop", "vcleave", "leave"]))
async def vc_stop(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        queues.pop(message.chat.id, None)
        loop_enabled.pop(message.chat.id, None)
        await message.reply("⏹ Stopped playback and left VC.")
    except GroupCallNotFoundError:
        await message.reply("❗ Not in a voice chat.")
    except Exception as e:
        await message.reply(f"❌ Couldn't stop VC: {e}")


@app.on_message(filters.command("skip"))
async def skip_song(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await play_next(message.chat.id)
        await message.reply("⏭ Skipped to next track.")
    except Exception as e:
        await message.reply(f"❌ Error skipping: {e}")


@app.on_message(filters.command("queue"))
async def show_queue(client, message):
    q = queues.get(message.chat.id)
    if not q or len(q) == 0:
        await message.reply("📭 Queue is empty.")
        return

    text = "🎶 Current Queue:\n"
    for i, song in enumerate(q):
        prefix = "▶" if i == 0 else f"{i+1}."
        text += f"{prefix} {song['title']}\n"
    await message.reply(text)


@app.on_message(filters.command("loop"))
async def toggle_loop(client, message):
    current = loop_enabled.get(message.chat.id, False)
    loop_enabled[message.chat.id] = not current
    status = "🔁 Loop enabled." if not current else "⏹ Loop disabled."
    await message.reply(status)


@app.on_message(filters.command("vcpause"))
async def vc_pause(client, message):
    try:
        await call_py.pause_stream(message.chat.id)
        await message.reply("⏸ Paused playback.")
    except Exception as e:
        await message.reply(f"❌ Error pausing: {e}")


@app.on_message(filters.command("vcresume"))
async def vc_resume(client, message):
    try:
        await call_py.resume_stream(message.chat.id)
        await message.reply("▶ Resumed playback.")
    except Exception as e:
        await message.reply(f"❌ Error resuming: {e}")


# === Start Bot ===
async def main():
    await app.start()
    await call_py.start()
    print("✅ Bot is running with PyTgCalls v2.2.5 compatibility...")
    await app.idle()

if _name_ == "_main_":
    asyncio.run(main())
