from tortoise import Tortoise, connections

from tgmusic.models.db.saved_track import SavedTrack
from .base_music_db import BaseMusicDB


class SQLiteMusicDB(BaseMusicDB):
    def __init__(self, path: str = 'tracks.db'):
        self.path = path


    async def init(self):
        await Tortoise.init(
            db_url = f'sqlite://{self.path}',
            modules = {'models': ['tgmusic.models.db.saved_track']}
        )

        await Tortoise.generate_schemas()

    
    async def save_track(self, track: SavedTrack):
        await track.save()

    
    async def get_track(self, id: str) -> SavedTrack:
        return await SavedTrack.filter(id = id).first()
    

    async def track_saved(self, id: str) -> bool:
        return await SavedTrack.exists(id = id)
    

    async def close(self):
        await connections.close_all()