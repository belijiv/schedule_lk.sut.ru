import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from selenium.webdriver.common.by import By

from bot.shared_data import attendance_service

router = Router()


@router.message(Command("check"))
@router.message(F.text == "🔍 Проверить пары")
async def cmd_check(message: Message, state: FSMContext):
    if not attendance_service.is_running:
        await message.answer("❌ Бот не запущен. Используйте /start")
        return

    await message.answer("🔍 <b>Запускаю ручную проверку пар...</b>", parse_mode="HTML")

    try:
        # Проверяем доступность драйвера
        if not attendance_service.driver:
            await message.answer("❌ Браузер не запущен. Перезапустите бота.")
            return

        # Обновляем страницу для актуального расписания
        attendance_service.driver.refresh()
        await asyncio.sleep(5)

        # Сначала проверяем внутривузовские пары
        intra_lesson = await attendance_service.find_current_lesson(False)
        if intra_lesson:
            response = (
                f"📚 <b>Найдена внутривузовская пара:</b>\n"
                f"<b>Предмет:</b> {intra_lesson['name']}\n"
                f"<b>Время:</b> {intra_lesson['time']}\n"
                f"<b>Тип:</b> {intra_lesson['type'] if 'type' in intra_lesson else 'Не указан'}"
            )

            # Проверяем наличие кнопки "Начать занятие"
            buttons_cell = intra_lesson['row'].find_element(By.XPATH, "./td[6]")
            buttons = buttons_cell.find_elements(By.TAG_NAME, "a")
            has_button = any("Начать занятие" in button.text for button in buttons)

            if has_button:
                response += "\n✅ <b>Кнопка 'Начать занятие' доступна</b>"
            else:
                response += "\n❌ <b>Кнопка 'Начать занятие' не доступна</b>"

            await message.answer(response, parse_mode="HTML")
            return  # Выходим после нахождения внутривузовской пары

        # Если внутривузовских пар нет, проверяем вневузовские
        extra_lesson = await attendance_service.find_current_lesson(True)
        if extra_lesson:
            response = (
                f"🏃 <b>Найдена вневузовская пара:</b>\n"
                f"<b>Предмет:</b> {extra_lesson['name']}\n"
                f"<b>Время:</b> {extra_lesson['time']}\n"
                f"<b>Тип:</b> {extra_lesson['type'] if 'type' in extra_lesson else 'Не указан'}"
            )

            # Проверяем наличие кнопки "Начать занятие"
            buttons_cell = extra_lesson['row'].find_element(By.XPATH, "./td[6]")
            buttons = buttons_cell.find_elements(By.TAG_NAME, "a")
            has_button = any("Начать занятие" in button.text for button in buttons)

            if has_button:
                response += "\n✅ <b>Кнопка 'Начать занятие' доступна</b>"
            else:
                response += "\n❌ <b>Кнопка 'Начать занятие' не доступна</b>"

            await message.answer(response, parse_mode="HTML")
            return  # Выходим после нахождения вневузовской пары

        # Если не найдено ни одной пары
        await message.answer("❌ <b>Пары не найдены</b>", parse_mode="HTML")

    except Exception as e:
        error_message = f"❌ <b>Ошибка при проверке пар:</b>\n{str(e)}"
        await message.answer(error_message, parse_mode="HTML")
        print(f"Ошибка в cmd_check: {e}")