from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_kb import get_main_keyboard
from bot.shared_data import attendance_service  # Используем общий экземпляр

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    success = await attendance_service.start()

    if success:
        welcome_text = (
            f"👋 <b>Привет, {user_name}!</b>\n\n"
            "🤖 <b>Бот для автоматической отметки на парах запущен!</b>\n\n"
            "📅 <b>Расписание проверок:</b>\n" +
            "\n".join([f"• {time}" for time in attendance_service.config.check_times]) +
            f"\n\n🏃 <b>Вневузовские пары:</b>\n" +
            "\n".join([f"• {time}" for time in attendance_service.config.extracurricular_times]) +
            "\n\n⚙️ <b>Настройки:</b>\n" +
            f"• Ожидание: {attendance_service.config.wait_time} мин\n" +
            f"• Интервал: {attendance_service.config.recheck_interval} мин\n" +
            f"• Повторы: {'∞' if attendance_service.config.max_iterations == -1 else attendance_service.config.max_iterations}\n\n"
            "📋 <b>Используйте кнопки для управления</b>"
        )
    else:
        welcome_text = (
            f"👋 <b>Привет, {user_name}!</b>\n\n"
            "❌ <b>Не удалось запустить систему!</b>\n\n"
            "Проверьте настройки и попробуйте /restart"
        )

    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )