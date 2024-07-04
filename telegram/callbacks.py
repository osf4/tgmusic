from aiogram.filters.callback_data import CallbackData
from music.playlist import PageAction

class PageCallback(CallbackData, prefix = 'page'):
    """Buttons that are used to change playlist pages"""

    action: PageAction
    playlist_id: str

class PageNumberCallback(CallbackData, prefix = 'pg_num'):
    """Button that shows pages in format 'current page/total pages'"""
    pass

class TrackCallback(CallbackData, prefix = 'track'):
    playlist_id: str
    track_id: str