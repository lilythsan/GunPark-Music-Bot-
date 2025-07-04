from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client["GunPark"]
