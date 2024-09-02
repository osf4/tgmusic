from abc import ABC, abstractmethod
from tgmusic.models.db.saved_track import SavedTrack


class BaseMusicDB(ABC):
    @abstractmethod
    async def init(self):
        pass


    @abstractmethod
    async def save_track(self, track: SavedTrack):
        pass


    @abstractmethod
    async def get_track(self, id: str) -> SavedTrack:
        pass


    @abstractmethod
    async def track_saved(self, id: str) -> bool:
        pass


    @abstractmethod
    async def close(self):
        pass