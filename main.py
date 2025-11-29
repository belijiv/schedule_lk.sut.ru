import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.middlewares.access_middleware import AccessMiddleware, CallbackAccessMiddleware
from bot.handlers.start import router as start_router
from bot.handlers.status import router as status_router
from bot.handlers.check import router as check_router
from bot.handlers.control import router as control_router
from bot.handlers.help import router as help_router
from bot.shared_data import attendance_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout
)

async def main():
    config = attendance_service.config

    bot = Bot(
        token=config.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация мидлварей
    dp.message.middleware(AccessMiddleware())
    dp.callback_query.middleware(CallbackAccessMiddleware())

    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(status_router)
    dp.include_router(check_router)
    dp.include_router(control_router)
    dp.include_router(help_router)

    try:
        logging.info(f"Бот запущен. Разрешенные пользователи: {config.allowed_user_ids}")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        await attendance_service.stop()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())