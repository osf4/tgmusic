from aiogram import Bot, Dispatcher
from contextlib import asynccontextmanager

from music.fetcher import Fetcher

async def __cleanup(bot: Bot, dp: Dispatcher, fetcher: Fetcher):
    await bot.delete_webhook()
    
    await dp.storage.close()
    await bot.session.close()
    
    await fetcher.close()

@asynccontextmanager
async def auto_cleanup(dp: Dispatcher, bot: Bot, fetcher: Fetcher):
    """
    Automatically clean up all resources acquired by 'dp', 'bot' and 'fetcher'
    """
    try:
        yield dp

    finally:
        await __cleanup(bot, dp, fetcher)