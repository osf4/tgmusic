import asyncio
import logging

from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config, CommandLinePaser
from vk.fetcher import VKFetcher

from telegram.handlers import router
from utils.auto_cleanup import auto_cleanup

async def main():
    command_line = CommandLinePaser()
    command_line.parse_args()

    config = Config()
    
    loaded = config.try_load(command_line.config_path)
    if loaded != True:
        print('Unable to load .env file! See --help command')
        return
    
    bot = Bot(token = config.tg_token, default = DefaultBotProperties(parse_mode = ParseMode.HTML))
    fetcher = VKFetcher(config.vk_token)
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    async with auto_cleanup(dp, bot, fetcher) as dp:
        await bot.delete_webhook(drop_pending_updates = True)
        await dp.start_polling(bot, allowed_updates = dp.resolve_used_update_types(), fetcher = fetcher)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with suppress(KeyboardInterrupt):
        asyncio.run(main())