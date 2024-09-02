from contextlib import suppress
from enum import StrEnum
from typing import Any
from aiovk import TokenSession, API

from validators import url as is_url
from urllib.parse import urlparse

from tgmusic.models.music.track_details import TrackDetails
from tgmusic.models.music.track import Track
from tgmusic.telegram.exceptions import UnparsableProfileURL

from .base_downloader import BaseDownloader, SearchResponse


class VKDownloader(BaseDownloader):
    class Methods(StrEnum):
        SEARCH = 'audio.search'
        GET_PLAYLIST_OF_USER = 'audio.get'
        GET_TRACK_BY_ID = 'audio.getById'

        GET_USER_INFO = 'users.get'


    def __init__(self, access_token: str):
        self.__session = TokenSession(access_token)
        self.__api = API(self.__session)
        

    async def search_tracks(self, 
                            query_or_owner_id: str | int, 
                            count: int = 10, 
                            offset: int = 0) -> SearchResponse:
        
        if self.__is_owner_id(query_or_owner_id):
            screen_name = self.__screen_name_from_url(query_or_owner_id)
            owner_id = await self.__get_owner_id(screen_name)

            return await self.__get_user_playlist(owner_id, count, offset)
        
        else:
            return await self.__search_by_query(query_or_owner_id, count, offset)
            

    async def __search_by_query(self, 
                                query: str, 
                                count: int = 10,
                                offset: int = 0) -> SearchResponse:

        response = await self.__request(self.Methods.SEARCH, 
                                        q = query,
                                        count = count,
                                        offset = offset)
        
        return self.__search_response_from_raw(response)

    
    async def __get_user_playlist(self, 
                                  owner_id: str | int, 
                                  count: int = 10, 
                                  offset: int = 0) -> SearchResponse:
        
        if isinstance(owner_id, str):
            owner_id = await self.__get_owner_id(owner_id)

        response = await self.__request(
            self.Methods.GET_PLAYLIST_OF_USER,
            owner_id = owner_id,
            count = count,
            offset = offset,
        )

        return self.__search_response_from_raw(response)

        

    async def get_details_by_id(self, id: str) -> TrackDetails:
        response = await self.__request(self.Methods.GET_TRACK_BY_ID,
                                        audios = id)
        
        track = response[0]

        details = TrackDetails(
            id = id,
            title = track['title'],
            artist = track['artist'],
            url = track['url'],
            thumbnail_url = self.__extract_thumbnail(track ),
        )

        return details


    async def close(self):
        await self.__session.close()


    async def __request(self, method: Methods, **params) -> dict[str, Any]:
        response = await self.__api(method, **params)
        return response
    

    def __is_owner_id(self, owner_id: str | int) -> bool:
        if isinstance(owner_id, str):
            return is_url(owner_id)
        
        return False


    def __screen_name_from_url(self, profile_url: str) -> str:
        """Return screen name of the user without '/' symbol at the beginning"""

        parsed_profile_url = urlparse(profile_url)
        if parsed_profile_url.netloc != 'vk.com' or parsed_profile_url.path == '':
            raise UnparsableProfileURL(f'can not parse profile URL: {profile_url}')
    
        return parsed_profile_url.path[1:]


    def __search_response_from_raw(self, response: dict[str, Any]) -> SearchResponse:
        tracks = [
            Track(
                id = self.__format_track_id(track['owner_id'], track['id']),
                title = track['title'],
                artist = track['artist'],
            ) for track in response['items']
        ]

        return SearchResponse(tracks, response['count'])


    def __format_track_id(self, owner: str, track: str) -> str:
        return f'{owner}_{track}'
    
    
    def __extract_thumbnail(self, raw_response: dict[str, Any]) -> str | None:
        with suppress(KeyError):
            return raw_response['album']['thumb']['photo_600']
        
        return None
    

    async def __get_owner_id(self, owner_screen_name: str) -> int:
        response = await self.__api(self.Methods.GET_USER_INFO, 
                                    user_ids = owner_screen_name)

        return response[0]['id']