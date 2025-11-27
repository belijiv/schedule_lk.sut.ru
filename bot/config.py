import os
import sys
from dataclasses import dataclass
from typing import List

# Добавляем корневую директорию в Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import config
except ImportError:
    print("❌ Ошибка: Не найден файл config.py в корне проекта")
    sys.exit(1)


@dataclass
class BotConfig:
    telegram_token: str
    chat_id: str
    allowed_user_ids: List[int]
    login: str
    password: str
    check_times: List[str]
    extracurricular_times: List[str]
    wait_time: int
    recheck_interval: int
    max_iterations: int
    edge_driver_path: str = None
    headless: bool = False
    webdriver_timeout: int = 10


def load_config() -> BotConfig:
    """Загружает конфигурацию из config.py"""
    required_fields = ['TELEGRAM_TOKEN', 'CHAT_ID', 'ALLOWED_USER_IDS', 'LOGIN', 'PASSWORD']

    for field in required_fields:
        if not hasattr(config, field):
            raise ValueError(f"❌ В config.py отсутствует поле: {field}")

    return BotConfig(
        telegram_token=config.TELEGRAM_TOKEN,
        chat_id=config.CHAT_ID,
        allowed_user_ids=config.ALLOWED_USER_IDS,
        login=config.LOGIN,
        password=config.PASSWORD,
        check_times=getattr(config, 'CHECK_TIMES', []),
        extracurricular_times=getattr(config, 'EXTRACURRICULAR_TIMES', []),
        wait_time=getattr(config, 'WAIT_TIME', 15),
        recheck_interval=getattr(config, 'RECHECK_INTERVAL', 10),
        max_iterations=getattr(config, 'MAX_ITERATIONS', -1),
        edge_driver_path=getattr(config, 'EDGE_DRIVER_PATH', None),
        headless=getattr(config, 'HEADLESS', False),
        webdriver_timeout=getattr(config, 'WEBDRIVER_TIMEOUT', 10)
    )