import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlitestorage import SQLiteStorage

from tgmusic.downloader.vk_downloader import VKDownloader
from tgmusic.db.sqlite_music_db import SQLiteMusicDB
from tgmusic.telegram.handlers import router

from tgmusic.config import Config
from tgmusic.utils import auto_cleanup


async def main():
    config = Config()

    bot = Bot(config.telegram_bot_token)
    dp = Dispatcher(storage = SQLiteStorage())
    
    dp.include_router(router)
    
    downloader = VKDownloader(config.vk_access_token)
    music_db = SQLiteMusicDB()
    
    async with auto_cleanup(bot, downloader, music_db):
        await dp.start_polling(bot, 
                            downloader = downloader,
                            music_db = music_db,
                            config = config)


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())