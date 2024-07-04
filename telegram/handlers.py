from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.filters import CommandStart, Command, CommandObject

from contextlib import suppress

from music.fetcher import Fetcher
from music.playlist import Playlist, default_page_size

from .markup import make_tracks_makrup 
from .callbacks import PageCallback, TrackCallback, PageNumberCallback

router = Router(name = __name__)

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!')

@router.message(Command('search'))
async def search_command_handler(msg: Message, command: CommandObject, fetcher: Fetcher, state: FSMContext):
    """
    Extract query from a message like '/search System of a down' and return playlist for 'System of a down'.
    """

    if command.args != None: 
        await __search_tracks_handler(
            query = command.args,
            msg = msg, 
            fetcher = fetcher,
            state = state)
    else:
        await msg.answer(f'Обязательно укажите ваш запрос\!\nК примеру, `/search Автостопом по фазе сна`', parse_mode = ParseMode.MARKDOWN_V2)


@router.message()
async def search_text_handler(msg: Message, fetcher: Fetcher, state: FSMContext):
   """
   Return a playlist for every text message from a user
   """

   await __search_tracks_handler(
       query = msg.text, 
       msg = msg, 
       fetcher = fetcher,
       state = state)

@router.callback_query(TrackCallback.filter())
async def track_callback_handler(query: CallbackQuery, callback_data: TrackCallback, 
                                 fetcher: Fetcher, state: FSMContext):
    await query.answer()

    try:
        playlist = await __get_playlist_from_FSM(state)
        if playlist.id_equals(callback_data.playlist_id) != True: # If user tries to push a button from previous playlist
            return

        track_url = await fetcher.get_url(callback_data.track_id)
        thumbnail_url = await __try_get_thumbnail_url(callback_data.track_id, fetcher)

        track = playlist.get_track_by_id(callback_data.track_id)

        audio = URLInputFile(track_url, chunk_size = 27350)
        thumbnail = URLInputFile(thumbnail_url) if thumbnail_url != '' else None

        await query.message.answer_audio(audio = audio, 
                                         title = track.title,
                                         thumbnail = thumbnail,
                                         performer = track.artist)

    except Exception:
        await query.message.answer(f'Упсс.. Что-то пошло не так... Попробуйте еще раз!')

@router.callback_query(PageCallback.filter())
async def page_callback_handler(query: CallbackQuery, callback_data: PageCallback, 
                                fetcher: Fetcher, state: FSMContext):
    await query.answer()

    with suppress(Exception):
        playlist = await __get_playlist_from_FSM(state)
        if playlist.id_equals(callback_data.playlist_id) != True: # If user tries to push a button from previous playlist
            return

        page_changed = playlist.change_page(callback_data.action)

        if page_changed:
            await __edit_playlist(query, fetcher, playlist)
            await __save_playlist_to_FSM(playlist, state)


@router.callback_query(PageNumberCallback.filter())
async def page_number_handle(query: CallbackQuery):
    await query.answer()

async def __try_get_thumbnail_url(id: str, fetcher: Fetcher) -> str:
    with suppress(Exception):
        return await fetcher.get_thumb_url(id)
    
    return ''

async def __search_tracks_handler(query: str, msg: Message, fetcher: Fetcher, state: FSMContext):
    """
    Search for a playlist by provided query and return a reply markup that allows to load tracks into the chat
    """
    
    try:
        tracks, total_count = await fetcher.search(
            query = query,
            count = default_page_size,
            offset = 0,
        )
        
        playlist = Playlist(
            id = str(msg.message_id),
            name = query,
            count = total_count,
            tracks = tracks,
        )

        await __save_playlist_to_FSM(playlist, state)

        await msg.answer(f'<b><i>{query}</i></b>',
                         reply_markup = make_tracks_makrup(playlist))
    
    except Exception:
        await msg.answer('Упс... Произошла ошибка во время поиска песен... Попробуйте еще раз!')


async def __edit_playlist(query: CallbackQuery, fetcher: Fetcher, playlist: Playlist):
    playlist.tracks, _ = await fetcher.search(
        query = playlist.name,
        count = default_page_size,
        offset = playlist.offset,
    )

    await query.message.edit_reply_markup(reply_markup = make_tracks_makrup(playlist))

async def __save_playlist_to_FSM(playlist: Playlist, state: FSMContext):
    await state.set_data({
        'playlist': playlist
    })

async def __get_playlist_from_FSM(state: FSMContext) -> Playlist:
    data = await state.get_data()
    return data['playlist']