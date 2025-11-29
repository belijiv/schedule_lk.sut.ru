from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_kb import get_main_keyboard

router = Router()


@router.message(Command("help"))
@router.message(F.text)  # Обрабатывает любой текст
async def handle_help_and_text(message: Message, state: FSMContext):
    # Очищаем состояние на всякий случай
    await state.clear()

    help_text = (
        "🤖 Используйте кнопки или команды:\n\n"
        "/start - запустить бота\n"
        "/status - статус бота\n"
        "/check - проверить пары\n"
        "/stop - остановить бота\n"
        "/restart - перезапустить бота\n\n"
        "📋 Или используйте кнопки меню ниже 👇"
    )

    await message.answer(
        help_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )