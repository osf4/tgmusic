from enum import StrEnum
from aiogram.fsm.context import FSMContext

from tgmusic.models.telegram.playlist import Playlist


class StateManager:
    class __Keys(StrEnum):
        CURRENT_PLAYLIST = 'current_playlist'


    @classmethod
    async def set_current_playlist(cls, state: FSMContext, playlist: Playlist):
        await state.set_data({
            cls.__Keys.CURRENT_PLAYLIST: playlist.model_dump_json(),
        })


    @classmethod
    async def get_current_playlist(cls, state: FSMContext) -> Playlist | None:
        data = await state.get_data()
        
        raw_playlist = data.get(cls.__Keys.CURRENT_PLAYLIST)
        return Playlist.model_validate_json(raw_playlist) if raw_playlist else None
    

    @classmethod
    async def current_playlist_exists(cls, state: FSMContext) -> bool:
        data = await state.get_data()
        return data.get(cls.__Keys.CURRENT_PLAYLIST) is not None