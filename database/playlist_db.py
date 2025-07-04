from .mongodb import db

playlists = db.playlists

async def save_playlist(user_id: int, name: str, songs: list):
    await playlists.update_one(
        {"user_id": user_id, "name": name},
        {"$set": {"songs": songs}},
        upsert=True
    )

async def get_playlist(user_id: int, name: str):
    data = await playlists.find_one({"user_id": user_id, "name": name})
    return data["songs"] if data else []
