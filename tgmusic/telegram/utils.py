from aiogram.types import URLInputFile

from tgmusic.db.base_music_db import BaseMusicDB
from tgmusic.models.db.saved_track import SavedTrack
from tgmusic.models.music.track_details import TrackDetails
from tgmusic.models.telegram.playlist import Playlist


async def __get_audio_by_id_or_db(track_details: TrackDetails,
                                  music_db: BaseMusicDB) -> str | URLInputFile:
    
    if not await music_db.track_saved(track_details.id):
        return URLInputFile(track_details.url, chunk_size = 27350)

    track = await music_db.get_track(track_details.id)
    return track.audio_file_id


async def __save_track(music_db: BaseMusicDB, id: str, audio_file_id: str):
    await music_db.save_track(
        SavedTrack(
            id = id,
            audio_file_id = audio_file_id,
        )
    )


def __input_file_if_url_not_none(url: str | None) -> URLInputFile | None:
    return URLInputFile(url) if url else None
        

def __via_caption_if_url_provided(bot_url: str | None) -> str | None:
   return f'[_via_]({bot_url})' if bot_url else None


def __playlist_not_exist_or_not_same(current_playlist: Playlist | None,
                                     playlist_id: str) -> bool:
    
    if not current_playlist:
        return False
    
    return not current_playlist.is_same_playlist(playlist_id)