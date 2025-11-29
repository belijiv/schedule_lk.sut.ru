from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Старт")],
            [KeyboardButton(text="⏸️ Остановить"), KeyboardButton(text="🔄 Перезапустить")],
            [KeyboardButton(text="📊 Статус"), KeyboardButton(text="🔍 Проверить пары")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
