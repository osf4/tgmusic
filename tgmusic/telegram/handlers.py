import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ErrorEvent
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from validators import url as is_url

from tgmusic.config import Config
from tgmusic.db.base_music_db import BaseMusicDB
from tgmusic.downloader.base_downloader import BaseDownloader

from tgmusic.models.telegram.playlist import Playlist

from tgmusic.telegram.keyboard.markup import tracks_markup
from tgmusic.telegram.keyboard.callbacks import NavigationAction
from tgmusic.telegram.keyboard.callbacks import NavigationButtonCallback, TrackCallback

from tgmusic.telegram.state_manager import StateManager
from tgmusic.telegram.utils import (__save_track, __get_audio_by_id_or_db, 
                    __input_file_if_url_not_none, __via_caption_if_url_provided,
                    __playlist_not_exist_or_not_same)


router = Router(name = __name__)


__greeting_message = """
👋🏻Привет, {first_name}!
Здесь ты можешь получить музыку из ВК прямо в Telegram.

• Введи название песни или исполнителя, и я отправлю тебе результаты по твоему запросу.
• Отправь ссылку на свой ВК, и я вышлю твой плейлист.
"""


@router.message(CommandStart())
async def handle_start(msg: Message, state: FSMContext):
    greeting = __greeting_message.format(
        first_name = msg.from_user.first_name,
    )

    await state.clear()
    await msg.answer(greeting)


@router.message()
async def handle_search(msg: Message, 
                        downloader: BaseDownloader, 
                        state: FSMContext):
    
    response = await downloader.search_tracks(msg.text)

    current_playlist = Playlist(
        query_message_id = msg.message_id,
        raw_query = msg.text,

        title = msg.text if not is_url(msg.text) else f'Музыка аккаунта\n{msg.text}',

        tracks = response.tracks,
        total_count = response.count, 
    )

    await StateManager.set_current_playlist(state, current_playlist)
    await msg.answer(current_playlist.title, 
                     reply_markup = tracks_markup(current_playlist))
        


@router.callback_query(TrackCallback.filter())
async def handle_track_callback(query: CallbackQuery, 
                                callback_data: TrackCallback,
                                downloader: BaseDownloader,
                                music_db: BaseMusicDB,
                                config: Config):
    
    track_details = await downloader.get_details_by_id(callback_data.track_id)
    audio = await __get_audio_by_id_or_db(track_details, music_db)

    send_audio = await query.message.answer_audio(
        audio = audio,
        thumbnail =  __input_file_if_url_not_none(track_details.thumbnail_url),

        title = track_details.title,
        performer = track_details.artist,
        
        caption = __via_caption_if_url_provided(config.telegram_bot_url),
        parse_mode = ParseMode.MARKDOWN_V2,
    )

    if not await music_db.track_saved(track_details.id):
        await __save_track(music_db, 
                           track_details.id,
                           send_audio.audio.file_id)

    await query.answer()


@router.callback_query(NavigationButtonCallback.filter())
async def handle_navigation_callback(query: CallbackQuery,
                                     callback_data: NavigationButtonCallback,
                                     downloader: BaseDownloader,
                                     state: FSMContext):
                                       
    current_playlist = await StateManager.get_current_playlist(state)
    if __playlist_not_exist_or_not_same(current_playlist,
                                        callback_data.playlist_id):
        
        await query.answer()
        return
    
    match callback_data.action:
        case NavigationAction.PREV:
            playlist_changed = current_playlist.move_back()

        case NavigationAction.NEXT:
            playlist_changed = current_playlist.move_next()


    if not playlist_changed:
        await query.answer()
        return
    
    response = await downloader.search_tracks(current_playlist.raw_query,
                                              offset = current_playlist.offset)
    
    current_playlist.update(new_tracks = response.tracks)
    await StateManager.set_current_playlist(state, current_playlist)

    await query.message.edit_reply_markup(
        reply_markup = tracks_markup(current_playlist),
    )
    
    await query.answer()


@router.error(F.update.message.as_('msg'))
async def handle_unknown_exception(event: ErrorEvent, msg: Message):
    logging.error(event.exception)

    await msg.answer('🙁Упс... Произошла неизвестная ошибка!\n✌️Попробуйте снова!')
