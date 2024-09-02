from aiogram import Bot, Dispatcher

from tgmusic.db.base_music_db import BaseMusicDB
from tgmusic.downloader.base_downloader import BaseDownloader

from contextlib import asynccontextmanager


@asynccontextmanager
async def auto_cleanup(bot: Bot, 
                       downloader: BaseDownloader,
                       music_db: BaseMusicDB):
    
    try:
        await bot.delete_webhook(drop_pending_updates = True)
        await music_db.init()

        yield

    finally:
        
        await bot.session.close()

        await downloader.close()
        await music_db.close()