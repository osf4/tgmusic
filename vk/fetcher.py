from music.fetcher import Fetcher
from music.track import Track
from aiovk import TokenSession, API


class VKFetcher(Fetcher):
    """
    VKFetcher searches for tracks using VK Audio api.
    """
    
    __session: TokenSession
    __api: API

    def __init__(self, access_token: str):
        self.__session = TokenSession(access_token)
        self.__api = API(self.__session)


    async def search(self, *, query: str, count: int = 3, offset: int = 0) -> tuple[list[Track], int]:
        response = await self.__api('audio.search', 
                             q = query, 
                             count = count, 
                             offset = offset)
        
        tracks = [Track(
            id = f'{track['owner_id']}_{track['id']}',
            artist = track['artist'],
            title = track['title'],
        ) for track in response['items']]
        
        return tracks, response['count']

    async def get_url(self, id: str) -> str:
        response = await self.__get_track_by_id(id)
        return response['url']
    
    async def get_thumb_url(self, id: str) -> str:
        response = await self.__get_track_by_id(id)
        return response['album']['thumb']['photo_68']


    async def __get_track_by_id(self, id: str) -> list[dict]:
        response = await self.__api('audio.getById', audios = id)
        return response[0]

    async def close(self):
        await self.__session.close()