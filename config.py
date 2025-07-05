import os
from dotenv import load_dotenv

# .env file load karo (isse private credentials fetch honge)
load_dotenv(dotenv_path=".env")

# Bot Configurations
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# MongoDB URI
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")

# Assistant VC Account Details
ASSISTANT_SESSION = os.getenv("ASSISTANT_SESSION")
ASSISTANT_API_ID = int(os.getenv("ASSISTANT_API_ID"))
ASSISTANT_API_HASH = os.getenv("ASSISTANT_API_HASH")
