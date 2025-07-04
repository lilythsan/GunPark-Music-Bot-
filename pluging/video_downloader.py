from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os

# 🔧 Set max limit (500MB)
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB in bytes

# 📦 Helper: Check file size before sending
def get_filesize(url):
    try:
        r = requests.head(url, allow_redirects=True)
        return int(r.headers.get("content-length", 0))
    except:
        return 0

# 🎥 YouTube Downloader
@Client.on_message(filters.command("ytdownload"))
async def youtube_downloader(client, message: Message):
    url = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else None
    if not url:
        return await message.reply("🎥 *YouTube link do!*\nUsage: `/ytdownload <link>`")

    msg = await message.reply("🔄 YouTube se video fetch ho raha hai...")
    try:
        video_url = f"https://example.com/dl?yt={url}"  # Replace with real parser
        file_size = get_filesize(video_url)

        if file_size > MAX_FILE_SIZE:
            await msg.edit(f"⚠️ File size 500MB se zyada hai.\n🔗 [Watch/Download here]({video_url})", disable_web_page_preview=True)
        else:
            await client.send_video(message.chat.id, video=video_url, caption="🎬 YouTube video lelo boss!")
            await msg.delete()
    except Exception as e:
        await msg.edit("❌ YouTube download failed.")
        print(f"[YT Error] {e}")

# 📸 Instagram Downloader
@Client.on_message(filters.command("instadownload"))
async def instagram_downloader(client, message: Message):
    url = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else None
    if not url:
        return await message.reply("📸 *Instagram link bhejo!*\nUsage: `/instadownload <link>`")

    msg = await message.reply("🔄 Insta se media le rahe hain...")
    try:
        media_url = f"https://example.com/dl?insta={url}"  # Replace with real parser
        file_size = get_filesize(media_url)

        if file_size > MAX_FILE_SIZE:
            await msg.edit(f"⚠️ File > 500MB hai.\n🔗 [Watch/Download]({media_url})", disable_web_page_preview=True)
        else:
            await client.send_video(message.chat.id, video=media_url, caption="📸 Insta video done!")
            await msg.delete()
    except Exception as e:
        await msg.edit("❌ Instagram download failed.")
        print(f"[Insta Error] {e}")

# 📌 Pinterest Downloader
@Client.on_message(filters.command("pindownload"))
async def pinterest_downloader(client, message: Message):
    url = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else None
    if not url:
        return await message.reply("📌 *Pinterest link paste karo!*\nUsage: `/pindownload <link>`")

    msg = await message.reply("🔄 Pinterest media ready ho raha hai...")
    try:
        pin_url = f"https://example.com/dl?pin={url}"  # Replace with real parser
        file_size = get_filesize(pin_url)

        if file_size > MAX_FILE_SIZE:
            await msg.edit(f"⚠️ File bada hai 500MB se.\n🔗 [Watch/Download]({pin_url})", disable_web_page_preview=True)
        else:
            await client.send_photo(message.chat.id, photo=pin_url, caption="📌 Pinterest image/video ready!")
            await msg.delete()
    except Exception as e:
        await msg.edit("❌ Pinterest download failed.")
        print(f"[Pin Error] {e}")
