from bot.services.attendance_service import AttendanceService
from bot.config import load_config

# Создаем общий экземпляр для всего приложения
config = load_config()
attendance_service = AttendanceService(config)