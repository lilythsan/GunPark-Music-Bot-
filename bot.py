import asyncio
import logging
from pyrogram import Client
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    OWNER_ID,
    ASSISTANT_SESSION,
    ASSISTANT_API_ID,
    ASSISTANT_API_HASH
)
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped  # ✅ Fixed this import
from pytgcalls.types.input_stream.quality import HighQualityAudio

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger("GunParkBot")
LOGGER.info("🔥 GunPark Bot Starting...")

# Main Bot
GunPark = Client(
    name="GunParkBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
)

# Assistant VC Client
Assistant = Client(
    name="assistant",
    api_id=ASSISTANT_API_ID,
    api_hash=ASSISTANT_API_HASH,
    session_string=ASSISTANT_SESSION
)

# VC Streaming Engine
VoiceCall = PyTgCalls(Assistant)

# Start everything
async def start_all():
    await Assistant.start()
    await GunPark.start()
    await VoiceCall.start()
    LOGGER.info("✅ GunPark + Assistant VC + VC Engine started.")
    await idle()

# Keep running
async def idle():
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await GunPark.stop()
        await Assistant.stop()
        LOGGER.info("🛑 Bot stopped.")

if _name_ == "_main_":
    asyncio.run(start_all())
