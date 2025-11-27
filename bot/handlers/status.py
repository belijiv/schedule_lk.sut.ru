from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.shared_data import attendance_service  # Общий экземпляр

router = Router()


@router.message(Command("status"))
@router.message(F.text == "📊 Статус")
async def cmd_status(message: Message, state: FSMContext):
    status_text = "🤖 <b>Статус бота:</b>\n\n"

    if attendance_service.is_running:
        status_text += "✅ <b>Бот активен</b>\n"

        if attendance_service.driver:
            status_text += "🌐 <b>Браузер запущен</b>\n"
        else:
            status_text += "❌ <b>Браузер не запущен</b>\n"

        next_check = attendance_service.get_next_check_time()
        status_text += f"⏰ <b>Следующая проверка:</b> {next_check}\n"

        # Добавляем отладочную информацию
        status_text += f"\n🔧 <b>Отладка:</b>\n"
        status_text += f"• is_running: {attendance_service.is_running}\n"
        status_text += f"• driver: {attendance_service.driver is not None}\n"

    else:
        status_text += "❌ <b>Бот остановлен</b>\n"
        status_text += "\nДля запуска используйте /start"

    await message.answer(status_text, parse_mode="HTML")