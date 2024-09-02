from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class NavigationAction(StrEnum):
    PREV = 'prev'
    NEXT = 'next'


class NavigationButtonCallback(CallbackData, prefix = 'nav'):
    action: NavigationAction
    playlist_id: int


class TrackCallback(CallbackData, prefix = 'track'):
    track_id: str
    playlist_id: int