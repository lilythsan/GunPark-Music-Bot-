from .mongodb import db

playlist_collection = db.playlists

async def save_playlist(user_id, playlist_name, songs):
    data = {
        "user_id": user_id,
        "playlist_name": playlist_name,
        "songs": songs,
    }
    await playlist_collection.insert_one(data)

async def get_playlists(user_id):
    return await playlist_collection.find({"user_id": user_id}).to_list(length=50)

async def delete_playlist(user_id, playlist_name):
    await playlist_collection.delete_one({"user_id": user_id, "playlist_name": playlist_name})
