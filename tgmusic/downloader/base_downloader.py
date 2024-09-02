from abc import ABC, abstractmethod
from typing import NamedTuple

from tgmusic.models.music.track import Track
from tgmusic.models.music.track_details import TrackDetails


SearchResponse = NamedTuple('SearchResponse',
                            [('tracks', list[Track]), ('count', int)])


class BaseDownloader(ABC):
    @abstractmethod
    async def search_tracks(self,
                            query_or_user_id: str | int,
                            count: int = 10,
                            offset: int = 0) -> SearchResponse:
        pass


    @abstractmethod
    async def get_details_by_id(self, id: str) -> TrackDetails:
        pass


    @abstractmethod
    async def close(self):
        pass