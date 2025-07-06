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
from pytgcalls.types.input_stream import AudioPiped
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
    name=ASSISTANT_SESSION,
    api_id=ASSISTANT_API_ID,
    api_hash=ASSISTANT_API_HASH,
    in_memory=True
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

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_all())



