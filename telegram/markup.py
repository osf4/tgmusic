from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from music.playlist import Playlist
from .callbacks import PageCallback, TrackCallback, PageNumberCallback, PageAction

def make_tracks_makrup(playlist: Playlist) -> InlineKeyboardMarkup:
      """
      Return markup with track buttons, navigation buttons and a page button.

      Every track button contains track-id and playlist-id in it's callback data
      """

      kb = InlineKeyboardBuilder()
      
      navigation_buttons = [
            InlineKeyboardButton(text = '⬅', 
                                 callback_data = PageCallback(action = PageAction.prev, playlist_id = playlist.id).pack()), 
            InlineKeyboardButton(text = '➡', 
                                 callback_data = PageCallback(action = PageAction.next, playlist_id = playlist.id).pack()),
      ]

      [kb.row(
            InlineKeyboardButton(
                  text = str(track),
                  callback_data = TrackCallback(playlist_id = playlist.id, track_id = track.id).pack(),
            )
      ) for track in playlist.tracks]

      page_num_button = InlineKeyboardButton(text = f'{playlist.page}/{playlist.total_pages}', 
                                             callback_data = PageNumberCallback().pack())

      kb.row(navigation_buttons[0], page_num_button, navigation_buttons[1])
      return kb.as_markup()