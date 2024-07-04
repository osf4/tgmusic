from abc import abstractmethod
from music.track import Track

class Fetcher:
    """
    Fetcher searches for tracks, returns their URLs, thumbs.  
    """

    @abstractmethod
    async def search(self, *, query: str, count: int, offset: int) -> list[Track]:
        pass

    @abstractmethod
    async def get_url(self, id: str) -> str:
        pass

    @abstractmethod
    async def get_thumb_url(self, id: str) -> str:
        pass

    @abstractmethod
    async def close():
        pass
