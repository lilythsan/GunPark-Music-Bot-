from .mongodb import db

users = db.users

async def add_user(user_id: int, username: str = ""):
    existing = await users.find_one({"user_id": user_id})
    if not existing:
        await users.insert_one({"user_id": user_id, "username": username})

async def get_user(user_id: int):
    return await users.find_one({"user_id": user_id})
