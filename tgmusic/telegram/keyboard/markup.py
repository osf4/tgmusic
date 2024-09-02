from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgmusic.models.telegram.playlist import Playlist
from .callbacks import TrackCallback, NavigationAction, NavigationButtonCallback


def tracks_markup(playlist: Playlist) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for track in playlist.tracks:
        kb.row(
            InlineKeyboardButton(
                text = str(track),
                callback_data = TrackCallback(
                    track_id = track.id,
                    playlist_id = playlist.query_message_id,
                ).pack(),
            ),
        )

    kb.row(
        InlineKeyboardButton(
            text = '↩',
            callback_data = NavigationButtonCallback(
                action = NavigationAction.PREV,
                playlist_id = playlist.query_message_id
            ).pack()
        ),

        InlineKeyboardButton(
            text = '↪',
            callback_data = NavigationButtonCallback(
                action = NavigationAction.NEXT,
                playlist_id = playlist.query_message_id,
            ).pack(),
        ))
    
    return kb.as_markup()