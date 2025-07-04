import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")

