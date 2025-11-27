import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_kb import get_main_keyboard
from bot.shared_data import attendance_service  # Общий экземпляр

router = Router()


@router.message(Command("stop"))
@router.message(F.text == "⏸️ Остановить")
async def cmd_stop(message: Message, state: FSMContext):
    if not attendance_service.is_running:
        await message.answer("❌ Бот уже остановлен")
        return

    success = await attendance_service.stop()
    if success:
        await message.answer("🛑 <b>Бот остановлен</b>", parse_mode="HTML")
    else:
        await message.answer("❌ <b>Не удалось остановить бота</b>", parse_mode="HTML")


@router.message(Command("restart"))
@router.message(F.text == "🔄 Перезапустить")
async def cmd_restart(message: Message, state: FSMContext):
    await message.answer("🔄 <b>Перезапускаю бота...</b>", parse_mode="HTML")

    # Останавливаем текущий экземпляр
    await attendance_service.stop()
    await asyncio.sleep(2)

    # Запускаем заново
    success = await attendance_service.start()

    if success:
        await message.answer(
            "✅ <b>Бот успешно перезапущен!</b>",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "❌ <b>Не удалось перезапустить бота</b>\nИспользуйте /start для повторной попытки.",
            parse_mode="HTML"
        )