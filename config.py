from pyrogram import filters
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=".env")

# Basic Bot Configuration
API_ID: int = int(os.getenv("API_ID", 0))
API_HASH: str = os.getenv("API_HASH", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
OWNER_ID: int = int(os.getenv("OWNER_ID", 0))
MONGO_DB_URI: str = os.getenv("MONGO_DB_URI", "")

# Optional future configs
# SUPPORT_GROUP: str = os.getenv("SUPPORT_GROUP", "")
# LOG_CHANNEL_ID: int = int(os.getenv("LOG_CHANNEL_ID", 0))
# DATABASE_NAME: str = os.getenv("DATABASE_NAME", "GunParkDB")

# Filters for Commands
COMMAND_FILTER = filters.command

