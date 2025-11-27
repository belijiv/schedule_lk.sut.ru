from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from bot.config import load_config

config = load_config()


class AccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id not in config.allowed_user_ids:
            await event.answer(
                "🚫 <b>Доступ запрещен!</b>\n\n"
                "У вас нет прав для использования этого бота.",
                parse_mode="HTML"
            )
            return

        return await handler(event, data)


class CallbackAccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id not in config.allowed_user_ids:
            await event.answer("🚫 У вас нет прав!", show_alert=True)
            return

        return await handler(event, data)